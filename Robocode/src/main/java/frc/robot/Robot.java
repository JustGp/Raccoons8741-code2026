// Copyright (c) FIRST and other WPILib contributors.
// Open Source Software; you can modify and/or share it under the terms of
// the WPILib BSD license file in the root directory of this project.

package frc.robot;

import edu.wpi.first.wpilibj.TimedRobot;
import edu.wpi.first.wpilibj.Timer;
import edu.wpi.first.wpilibj2.command.Command;
import edu.wpi.first.wpilibj2.command.CommandScheduler;
import edu.wpi.first.wpilibj.XboxController;
import edu.wpi.first.wpilibj.drive.DifferentialDrive;
import edu.wpi.first.wpilibj.motorcontrol.PWMSparkMax;
import edu.wpi.first.wpilibj.motorcontrol.Spark;

import static edu.wpi.first.units.Units.Volt;

import com.fasterxml.jackson.annotation.Nulls;
import com.revrobotics.spark.SparkMax;
import com.revrobotics.spark.SparkLowLevel.MotorType;

import edu.wpi.first.wpilibj.RobotController;

/*
 *          Hello!!!
 * at the movement of the robot
 *  (-) is forward ( towards the eater side)
 * 
 * 
 * At the main shooter
 * (+) Shoot and grab
 * (-)Spit
 * 
 * At the directioner 
 * (+)In
 * (-) Out
 * 
 * 
 * Controller controls:
 * 
 * 
 */

/**
 * The methods in this class are called automatically corresponding to each mode, as described in
 * the TimedRobot documentation. If you change the name of this class or the package after creating
 * this project, you must also update the Main.java file in the project.
 */
public class Robot extends TimedRobot {
  private final SparkMax m_leftDrive = new SparkMax(1, MotorType.kBrushed);
  private final SparkMax m_rightDrive = new SparkMax(2, MotorType.kBrushed);

  //Setting up the motors 
  private final SparkMax main_launcher = new SparkMax(5, MotorType.kBrushless);
  private final SparkMax directioner = new SparkMax(6, MotorType.kBrushless);

  private XboxController m_controller = new XboxController(0);

  private final DifferentialDrive m_robotDrive =  new DifferentialDrive(m_leftDrive::set, m_rightDrive::set);

  private Command m_autonomousCommand;

  private final RobotContainer m_robotContainer;

  private final Timer m_timer = new Timer();

  private double StartTime;
  private double realtime;

  private final double drift_fix = 0.13955;

  private final double drift2 = -0.13955;
// For autonomous
  private double EffectiveVoltage = 8;
  private double Voltage = 0;
  private double PercentageVoltage = 0;




  private double velocity = 0.5;
  /**
   * This function is run when the robot is first started up and should be used for any
   * initialization code.
   */
  public Robot() {
    // Instantiate our RobotContainer.  This will perform all our button bindings, and put our
    // autonomous chooser on the dashboard.
      m_rightDrive.setInverted(true);
    m_robotContainer = new RobotContainer();
  }

  /**
   * This function is called every 20 ms, no matter the mode. Use this for items like diagnostics
   * that you want ran during disabled, autonomous, teleoperated and test.
   *
   * <p>This runs after the mode specific periodic functions, but before LiveWindow and
   * SmartDashboard integrated updating.
   */
  @Override
  public void robotPeriodic() {
    // Runs the Scheduler.  This is responsible for polling buttons, adding newly-scheduled
    // commands, running already-scheduled commands, removing finished or interrupted commands,
    // and running subsystem periodic() methods.  This must be called from the robot's periodic
    // block in order for anything in the Command-based framework to work.
    CommandScheduler.getInstance().run();
  }

  /** This function is called once each time the robot enters Disabled mode. */
  @Override
  public void disabledInit() {}

  @Override
  public void disabledPeriodic() {}

  /** This autonomous runs the autonomous command selected by your {@link RobotContainer} class. */
  @Override
  public void autonomousInit() {
    m_autonomousCommand = m_robotContainer.getAutonomousCommand();

    // schedule the autonomous command (example)
    if (m_autonomousCommand != null) {
      CommandScheduler.getInstance().schedule(m_autonomousCommand);
    }
    StartTime = System.currentTimeMillis();

    m_timer.reset();
    m_timer.start();

    //Get the voltage from the battery and calculate the effective voltage for the motors
    Voltage = RobotController.getBatteryVoltage();
    PercentageVoltage = EffectiveVoltage/Voltage;
    System.out.println("Percentage voltage: " + PercentageVoltage);

    //Formula for distance, calculator adjunted in the github
    //a+b(PV)+c*t+d(PV*t)+e(PV^2)*t

  }

  /** This function is called periodically during autonomous. */
  @Override
  public void autonomousPeriodic() {
    double time = Timer.getFPGATimestamp();
    realtime = time - StartTime;
    System.out.println(m_timer.get());



    if ((m_timer.get()) < 2.0) {
      m_robotDrive.arcadeDrive(-PercentageVoltage, drift2);
      System.out.println(realtime);
    } 
    else{
      m_robotDrive.arcadeDrive(0, 0);

    }
    








  }


  @Override
  public void teleopInit() {
    // This makes sure that the autonomous stops running when
    // teleop starts running. If you want the autonomous to
    // continue until interrupted by another command, remove
    // this line or comment it out.
    if (m_autonomousCommand != null) {
      m_autonomousCommand.cancel();
    }
  }

  /** This function is called periodically during operator control. */
  @Override
  public void teleopPeriodic() 
  {

   m_robotDrive.arcadeDrive(m_controller.getLeftY()*0.7, m_controller.getRightX()*0.7);
   System.out.println(m_controller.getLeftY());



   




  //shoot
  if(m_controller.getRightBumper()){
    directioner.set(0);
    main_launcher.set(0);


    directioner.set(-1);
    main_launcher.set(1);// to laucnh put 1
  }


  //off
  if(m_controller.getBButton()){
    directioner.set(0);
    main_launcher.set(0);

  }

  //grab n store aka eat

  if(m_controller.getXButton()){
    directioner.set(0);
    main_launcher.set(0);


    directioner.set(0.6);
    main_launcher.set(0.3);//negative
  }
//spit
  if (m_controller.getYButton()){
    directioner.set(0);
    main_launcher.set(0);

    directioner.set(0.5);
    main_launcher.set(-0.55);

  }
  
}


  @Override
  public void testInit() {
    // Cancels all running commands at the start of test mode.
    CommandScheduler.getInstance().cancelAll();
  }

  /** This function is called periodically during test mode. */
  @Override
  public void testPeriodic() {}

  /** This function is called once when the robot is first started up. */
  @Override
  public void simulationInit() {}

  /** This function is called periodically whilst in simulation. */
  @Override
  public void simulationPeriodic() {}
}