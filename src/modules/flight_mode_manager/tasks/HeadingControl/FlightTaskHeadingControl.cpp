// Flight Task Heading Control

#include "FlightTaskHeadingControl.hpp"
#include <mathlib/mathlib.h>
#include <cmath>

bool FlightTaskHeadingControl::activate(vehicle_local_position_setpoint_s last_setpoint)
{
  _position_setpoint(0) = NAN;
  _position_setpoint(1) = NAN;
  _position_setpoint(2) = -1.5f;
  _yaw_setpoint = 130.0f*3.142f/180.f;
  return true;
}

bool FlightTaskHeadingControl::update()
{
  _yaw_setpoint = 130.0f * 3.142f/180.0f;
  _position_setpoint(0) = NAN;
  _position_setpoint(1) = NAN;
  _position_setpoint(2) = -1.5f; // NED coordinates
  _velocity_setpoint(0) = 1.0f * cos(_yaw_setpoint);
  _velocity_setpoint(1) = 1.0f * sin(_yaw_setpoint);
  _velocity_setpoint(2) = 0.0f;
  return true;
}

