// Flight Task Heading Control

#include "FlightTaskHeadingControl.hpp"
#include <mathlib/mathlib.h>
#include <cmath>
#include <uORB/topics/transponder_report.h>
#include <uORB/Subscription.hpp>
#include <uORB/uORB.h>


bool FlightTaskHeadingControl::activate(vehicle_local_position_setpoint_s last_setpoint)
{
  _position_setpoint(0) = NAN;
  _position_setpoint(1) = NAN;
  _position_setpoint(2) = -1.5f;
  return true;
}

bool FlightTaskHeadingControl::update()
{
  uORB::Subscription _transponder_report_sub{ORB_ID(transponder_report)};
  transponder_report_s pos;

  if(_transponder_report_sub.update(&pos)){
    _yaw_setpoint = pos.heading + 3.142f;
    _velocity_setpoint(0) = pos.hor_velocity * cos(_yaw_setpoint);
    _velocity_setpoint(1) = pos.hor_velocity * sin(_yaw_setpoint);
    _position_setpoint(0) = NAN;
    _position_setpoint(1) = NAN;
    _position_setpoint(2) = -1.0f * pos.altitude; // NED coordinates
  }

  _velocity_setpoint(2) = 0.0f;
  if(_yaw_setpoint == NAN){
    _velocity_setpoint(0) = 0;
    _velocity_setpoint(1) = 0;
    _position_setpoint(0) = 0;
    _position_setpoint(1) = 0;
    _position_setpoint(2) = -1.5f; // NED coordinates
  }

  return true;
}
