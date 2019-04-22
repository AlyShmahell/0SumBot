# Copyright 2010 owners of the AI Challenge project
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy
# of the License at http:#www.apache.org/licenses/LICENSE-2.0 . Unless
# required by applicable law or agreed to in writing, software distributed
# under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.
#
# Author: Jeff Cameron (jeff@jpcameron.com)
#
# Makefile for the Tic-Tac-Toe contest engine.
# this Makefile was modified on Nov 30th 2017 by Aly Shmahell to remove Java KeyStore features.

TARGETS = Visualizer.jar PlayGame.jar ShowGame.jar

all: $(TARGETS)

clean:
	rm -f *.class *.html
	mv *.jar ../build/

CLViewer.class: VizPanel.class ViewerPanel.class Viewer.java Game.class CLViewer.java
	javac CLViewer.java

Engine.class: Engine.java Game.class
	javac Engine.java

Fleet.class: Fleet.java
	javac Fleet.java

Game.class: Fleet.class Game.java Planet.class
	javac Game.java

Planet.class: Planet.java
	javac Planet.java

PlayGame.jar: Engine.class
	jar cfe PlayGame.jar Engine *.class

RenderMap.class: RenderMap.java Game.class
	javac RenderMap.java

ShowGame.jar: CLViewer.class ViewerPanel.class VizPanel.class
	jar cfe ShowGame.jar CLViewer *.class img/*.png img/*.jpg img/*.gif

Viewer.class: VizPanel.class ViewerPanel.class Viewer.java Game.class
	javac Viewer.java

ViewerPanel.class: ViewerPanel.java
	javac ViewerPanel.java

Visualizer.jar: Viewer.class AppletManifest.txt
	jar cfvm Visualizer.jar AppletManifest.txt *.class img/*.png img/*.jpg img/*.gif

VizPanel.class: VizPanel.java
	javac VizPanel.java
