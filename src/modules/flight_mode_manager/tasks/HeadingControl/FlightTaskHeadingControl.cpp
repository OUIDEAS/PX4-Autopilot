// Flight Task Heading Control

#include "FlightTaskHeadingControl.hpp"
#include <mathlib/mathlib.h>
#include <cmath>
#include <uORB/topics/manual_control_setpoint.h>
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
  uORB::Subscription _manual_control_setpoint_sub{ORB_ID(manual_control_setpoint)};
  manual_control_setpoint_s pos;

  if(_manual_control_setpoint_sub.update(&pos)){
    _yaw_setpoint = pos.x;
    _velocity_setpoint(0) = pos.z * cos(_yaw_setpoint);
    _velocity_setpoint(1) = pos.z * sin(_yaw_setpoint);
    _position_setpoint(0) = NAN;
    _position_setpoint(1) = NAN;
    _position_setpoint(2) = -1.0f * pos.y; // NED coordinates
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
