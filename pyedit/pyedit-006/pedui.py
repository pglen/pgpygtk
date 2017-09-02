#!/usr/bin/env python

# Menu items for the pyedit project

''' 
    <menuitem action='Stop'/>
      <menu action='ColorMenu'>
        <menuitem action='Red'/>
        <menuitem action='Green'/>
        <menuitem action='Blue'/>
    </menu>
      <menu action='ShapeMenu'>
        <menuitem action='Square'/>
        <menuitem action='Rectangle'/>
        <menuitem action='Oval'/>
        <menuitem action='Bold'/>
      </menu>
'''
         
ui_info = \
'''<ui>
  <menubar name='MenuBar'>
    <menu action='FileMenu'>
      <menuitem action='New'/>
      <menuitem action='Open'/>
      <menuitem action='Close'/>
      <menuitem action='Save'/>
      <menuitem action='SaveAs'/>
      <separator/>
      <menuitem action='Quit'/>
      <menuitem action='Exit'/>
    </menu>

    <menu action='EditMenu'>
      <menuitem action='Cut'/>
      <menuitem action='Copy'/>
      <menuitem action='Paste'/>
    </menu>

    <menu action='NavMenu'>
      <menuitem action='Goto'/>
      <menuitem action='Find'/>
    </menu>
   
    <menu action='MacrosMenu'>
      <menuitem action='Record'/>
      <menuitem action='Play'/>
      <menuitem action='Animate'/>
      <menuitem action='Savemacro'/>
      <menuitem action='Loadmacro'/>
    </menu>

    <menu action='PreferencesMenu'>     
        <menuitem action='Colors'/>
        <menuitem action='Fonts'/>
      </menu>

    <menu action='HelpMenu'>
      <menuitem action='Help'/>
      <menuitem action='QuickHelp'/>
      <separator/>
      <menuitem action='About'/>      
    </menu>
  </menubar>

  <toolbar  name='ToolBar'>
    <toolitem action='New'/>
    <toolitem action='Open'/>
    <toolitem action='Quit'/>
    <separator/>
    <toolitem action='Logo'/>
  </toolbar>
</ui>'''

