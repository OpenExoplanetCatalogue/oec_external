#!/usr/bin/python
import openexoplanetcatalogue
import exoplaneteu
import exoplanetarchive

openexoplanetcatalogue.get()
openexoplanetcatalogue.parse()
	
exoplaneteu.get()
exoplaneteu.parse()

exoplanetarchive.get()
exoplanetarchive.parse()


