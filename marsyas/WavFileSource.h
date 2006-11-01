/*
** Copyright (C) 1998-2006 George Tzanetakis <gtzan@cs.uvic.ca>
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

/**
   \class WavFileSource
   \brief SoundFileSource for .wav soundfiles
   
   SoundFileSource reader for .wav sound files.
*/

#ifndef MARSYAS_WAVFILESOURCE_H
#define MARSYAS_WAVFILESOURCE_H

#include "common.h"
#include "AbsSoundFileSource.h"

#include <string>
#include <cstdio>

namespace Marsyas
{

class WavFileSource: public AbsSoundFileSource
{
private:
  short *sdata_;
  unsigned char *cdata_;
  
	FILE *sfp_;
  long sfp_begin_;
  
  mrs_natural sampleSize_; //in bytes
  mrs_natural csize_;
  mrs_natural size_;  
  short sval_;
  unsigned short bits_;

  void addControls();
	void myUpdate();
  unsigned long ByteSwapLong(unsigned long nLongNumber);
  unsigned short ByteSwapShort (unsigned short nValue);
  
  mrs_natural nChannels_;
  mrs_natural inSamples_;
  mrs_natural samplesToRead_;
  mrs_natural samplesRead_;
  mrs_natural samplesToWrite_;

  mrs_natural samplesOut_;
  
  mrs_real repetitions_;
  mrs_real duration_;
  
public:
  WavFileSource(std::string name);
  ~WavFileSource();
  MarSystem* clone() const;  

  mrs_natural getLinear16(realvec& win); //private [?]
  mrs_natural getLinear8(mrs_natural c, realvec& win); //private [?]

  void getHeader(std::string filename);
  void myProcess(realvec& in, realvec &out);
};

}//namespace Marsyas


#endif     /* !MARSYAS_WAVFILESOURCE_H */ 

	
