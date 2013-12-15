/*
** Copyright (C) 1998-2005 George Tzanetakis <gtzan@cs.uvic.ca>
**
** This program is free software; you can redistribute it and/or modify
** it under the terms of the GNU General Public License as published by
** the Free Software Foundation; either version 2 of the License, or
** (at your option) any later version.
**
** This program is distributed in the hope that it will be useful,
** but WITHOUT ANY WARRANTY; without even the implied warranty of
** MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
** GNU General Public License for more details.
**
** You should have received a copy of the GNU General Public License
** along with this program; if not, write to the Free Software
** Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
*/

#ifndef MARSYAS_SVFILTER_H
#define MARSYAS_SVFILTER_H

#include <marsyas/system/MarSystem.h>
#include <cmath>

namespace Marsyas
{
/**
	yl(n) = Fyb(n) + yl(n-1)
	yb(n) = Fyh(n) + yb(n-1)
	yh(n) = x(n) - yl(n-1) - Qyb(n-1)

	F = 2sin(pi*fc/fs)
	Q = 2*damp

	\ingroup Processing
	\brief State Variable Filter

TODO: Put something descriptive here!

*/

class SVFilter: public MarSystem
{
private:
  void addControls();

  mrs_bool freqIn_;
  mrs_natural type_;

  mrs_real israte_;
  mrs_real frequency_;
  mrs_real res_ = 0.1;

	mrs_real notch = 0.0;
	mrs_real low = 0.0;
	mrs_real high = 0.0;
	mrs_real band = 0.0;

public:
  SVFilter(std::string name);
  ~SVFilter();
  MarSystem* clone() const;

  void myUpdate(MarControlPtr sender);
  void myProcess(realvec& in, realvec& out);
};

} // namespace Marsyas

#endif
