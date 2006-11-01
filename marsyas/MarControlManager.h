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

/** 
\class MarControlManager
\brief MarControlManager handle controls creation
\author lmartins@inescporto.pt, lfpt@inescporto.pt
**/

#ifndef MARSYAS_MARCONTROLMANAGER_H
#define MARSYAS_MARCONTROLMANAGER_H

#include <map>
#include <vector>
#include "MarControl.h"

namespace Marsyas
{
	class MarSystem;

	class MarControlManager
	{
	protected:
		std::map<std::string, MarControlPtr> registry;
		//std::map<std::string, MarControlValue*> workingSet; 

	public:
		MarControlManager();
		~MarControlManager();
		void registerPrototype(std::string name, MarControlPtr);
		MarControlPtr getPrototype(std::string type);
		MarControlPtr create(std::string type, std::string name, MarSystem *msys, bool state);
		MarControlPtr getMarSystem(std::istream& is);

		//std::map<std::string, MarSystem*> getWorkingSet(std::istream& is);

		bool isRegistered (std::string name);

		std::vector <std::string> registeredPrototypes(); 
	};

}

#endif /* MARSYAS_MARCONTROLMANAGER_H	*/