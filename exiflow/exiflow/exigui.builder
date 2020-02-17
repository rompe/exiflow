<?xml version="1.0" encoding="UTF-8"?>
<!-- Generated with glade 3.22.1 -->
<!--*- mode: xml -*-->
<interface>
  <requires lib="gtk+" version="3.0"/>
  <object class="GtkAboutDialog" id="aboutdialog1">
    <property name="visible">True</property>
    <property name="can_focus">False</property>
    <property name="window_position">center-on-parent</property>
    <property name="destroy_with_parent">True</property>
    <property name="type_hint">normal</property>
    <property name="program_name">ExiFlow</property>
    <property name="version">0.4.5.16</property>
    <property name="copyright" translatable="yes">© Copyright 2006-2014. Some rights reserved.</property>
    <property name="comments" translatable="yes">This is a beta version. Use at your own risk.</property>
    <property name="website">http://exiflow.org/</property>
    <property name="website_label" translatable="yes">Exiflow Homepage</property>
    <property name="license">    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, write to the Free Software
    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
</property>
    <property name="authors">Sebastian Berthold
Ulf Rompe</property>
    <property name="translator_credits" translatable="yes" comments="TRANSLATORS: Replace this string with your names, one name per line.">translator-credits</property>
    <property name="logo_icon_name">image-missing</property>
    <child>
      <placeholder/>
    </child>
    <child internal-child="vbox">
      <object class="GtkBox" id="dialog-vbox2">
        <property name="can_focus">False</property>
        <child internal-child="action_area">
          <object class="GtkButtonBox" id="dialog-action_area2">
            <property name="can_focus">False</property>
          </object>
          <packing>
            <property name="expand">False</property>
            <property name="fill">False</property>
            <property name="pack_type">end</property>
            <property name="position">0</property>
          </packing>
        </child>
      </object>
    </child>
  </object>
  <object class="GtkFileChooserDialog" id="directorychooserdialog1">
    <property name="can_focus">False</property>
    <property name="type_hint">dialog</property>
    <property name="action">select-folder</property>
    <property name="select_multiple">True</property>
    <signal name="response" handler="on_directorychooserdialog1_response" object="bla" swapped="yes"/>
    <child internal-child="vbox">
      <object class="GtkBox" id="vbox12">
        <property name="visible">True</property>
        <property name="can_focus">False</property>
        <property name="spacing">24</property>
        <child internal-child="action_area">
          <object class="GtkButtonBox" id="hbuttonbox1">
            <property name="visible">True</property>
            <property name="can_focus">False</property>
            <property name="layout_style">end</property>
            <child>
              <object class="GtkButton" id="button6">
                <property name="label">gtk-cancel</property>
                <property name="visible">True</property>
                <property name="can_focus">True</property>
                <property name="can_default">True</property>
                <property name="receives_default">False</property>
                <property name="use_stock">True</property>
              </object>
              <packing>
                <property name="expand">True</property>
                <property name="fill">True</property>
                <property name="position">0</property>
              </packing>
            </child>
            <child>
              <object class="GtkButton" id="button7">
                <property name="label">gtk-open</property>
                <property name="visible">True</property>
                <property name="can_focus">True</property>
                <property name="can_default">True</property>
                <property name="has_default">True</property>
                <property name="receives_default">False</property>
                <property name="use_stock">True</property>
              </object>
              <packing>
                <property name="expand">True</property>
                <property name="fill">True</property>
                <property name="position">1</property>
              </packing>
            </child>
          </object>
          <packing>
            <property name="expand">False</property>
            <property name="fill">False</property>
            <property name="pack_type">end</property>
            <property name="position">0</property>
          </packing>
        </child>
      </object>
    </child>
    <action-widgets>
      <action-widget response="-6">button6</action-widget>
      <action-widget response="-5">button7</action-widget>
    </action-widgets>
  </object>
  <object class="GtkFileChooserDialog" id="filechooserdialog1">
    <property name="can_focus">False</property>
    <property name="type_hint">dialog</property>
    <property name="select_multiple">True</property>
    <signal name="response" handler="on_filechooserdialog1_response" object="bla" swapped="yes"/>
    <child internal-child="vbox">
      <object class="GtkBox" id="dialog-vbox1">
        <property name="visible">True</property>
        <property name="can_focus">False</property>
        <property name="spacing">24</property>
        <child internal-child="action_area">
          <object class="GtkButtonBox" id="dialog-action_area1">
            <property name="visible">True</property>
            <property name="can_focus">False</property>
            <property name="layout_style">end</property>
            <child>
              <object class="GtkButton" id="button1">
                <property name="label">gtk-cancel</property>
                <property name="visible">True</property>
                <property name="can_focus">True</property>
                <property name="can_default">True</property>
                <property name="receives_default">False</property>
                <property name="use_stock">True</property>
              </object>
              <packing>
                <property name="expand">True</property>
                <property name="fill">True</property>
                <property name="position">0</property>
              </packing>
            </child>
            <child>
              <object class="GtkButton" id="button2">
                <property name="label">gtk-open</property>
                <property name="visible">True</property>
                <property name="can_focus">True</property>
                <property name="can_default">True</property>
                <property name="has_default">True</property>
                <property name="receives_default">False</property>
                <property name="use_stock">True</property>
              </object>
              <packing>
                <property name="expand">True</property>
                <property name="fill">True</property>
                <property name="position">1</property>
              </packing>
            </child>
          </object>
          <packing>
            <property name="expand">False</property>
            <property name="fill">False</property>
            <property name="pack_type">end</property>
            <property name="position">0</property>
          </packing>
        </child>
      </object>
    </child>
    <action-widgets>
      <action-widget response="-6">button1</action-widget>
      <action-widget response="-5">button2</action-widget>
    </action-widgets>
  </object>
  <object class="GtkWindow" id="mainwindow">
    <property name="visible">True</property>
    <property name="can_focus">False</property>
    <property name="title" translatable="yes">exiflow - exigui</property>
    <property name="default_width">500</property>
    <property name="default_height">600</property>
    <signal name="destroy" handler="on_mainwindow_destroy" swapped="no"/>
    <child>
      <placeholder/>
    </child>
    <child>
      <object class="GtkVBox" id="vbox1">
        <property name="visible">True</property>
        <property name="can_focus">False</property>
        <child>
          <object class="GtkMenuBar" id="menubar1">
            <property name="visible">True</property>
            <property name="can_focus">False</property>
          </object>
          <packing>
            <property name="expand">False</property>
            <property name="fill">False</property>
            <property name="position">0</property>
          </packing>
        </child>
        <child>
          <object class="GtkVPaned" id="vpaned1">
            <property name="visible">True</property>
            <property name="can_focus">True</property>
            <property name="position">180</property>
            <child>
              <object class="GtkFrame" id="frame2">
                <property name="visible">True</property>
                <property name="can_focus">False</property>
                <property name="label_xalign">0</property>
                <child>
                  <object class="GtkAlignment" id="alignment2">
                    <property name="visible">True</property>
                    <property name="can_focus">False</property>
                    <property name="left_padding">12</property>
                    <child>
                      <object class="GtkHBox" id="hbox2">
                        <property name="visible">True</property>
                        <property name="can_focus">False</property>
                        <child>
                          <object class="GtkScrolledWindow" id="scrolledwindow1">
                            <property name="visible">True</property>
                            <property name="can_focus">True</property>
                            <property name="shadow_type">in</property>
                            <child>
                              <object class="GtkTreeView" id="treeview1">
                                <property name="visible">True</property>
                                <property name="can_focus">True</property>
                                <property name="headers_visible">False</property>
                                <child internal-child="selection">
                                  <object class="GtkTreeSelection"/>
                                </child>
                              </object>
                            </child>
                          </object>
                          <packing>
                            <property name="expand">True</property>
                            <property name="fill">True</property>
                            <property name="position">0</property>
                          </packing>
                        </child>
                        <child>
                          <object class="GtkVBox" id="vbox2">
                            <property name="visible">True</property>
                            <property name="can_focus">False</property>
                            <child>
                              <placeholder/>
                            </child>
                            <child>
                              <object class="GtkButton" id="button3">
                                <property name="label">gtk-open</property>
                                <property name="visible">True</property>
                                <property name="can_focus">True</property>
                                <property name="focus_on_click">False</property>
                                <property name="receives_default">False</property>
                                <property name="use_stock">True</property>
                                <signal name="clicked" handler="on_button_open_clicked" swapped="no"/>
                              </object>
                              <packing>
                                <property name="expand">False</property>
                                <property name="fill">False</property>
                                <property name="position">1</property>
                              </packing>
                            </child>
                            <child>
                              <placeholder/>
                            </child>
                          </object>
                          <packing>
                            <property name="expand">False</property>
                            <property name="fill">False</property>
                            <property name="padding">5</property>
                            <property name="position">1</property>
                          </packing>
                        </child>
                      </object>
                    </child>
                  </object>
                </child>
                <child type="label">
                  <object class="GtkLabel" id="label8">
                    <property name="visible">True</property>
                    <property name="can_focus">False</property>
                    <property name="label" translatable="yes">Pathes</property>
                  </object>
                </child>
              </object>
              <packing>
                <property name="resize">True</property>
                <property name="shrink">True</property>
              </packing>
            </child>
            <child>
              <object class="GtkVBox" id="vbox7">
                <property name="visible">True</property>
                <property name="can_focus">False</property>
                <child>
                  <object class="GtkNotebook" id="notebook1">
                    <property name="visible">True</property>
                    <property name="can_focus">True</property>
                    <child>
                      <object class="GtkVBox" id="vbox11">
                        <property name="visible">True</property>
                        <property name="can_focus">False</property>
                        <child>
                          <object class="GtkFrame" id="frame13">
                            <property name="visible">True</property>
                            <property name="can_focus">False</property>
                            <property name="label_xalign">0</property>
                            <child>
                              <object class="GtkAlignment" id="alignment13">
                                <property name="visible">True</property>
                                <property name="can_focus">False</property>
                                <property name="left_padding">12</property>
                                <child>
                                  <object class="GtkHBox" id="hbox17">
                                    <property name="visible">True</property>
                                    <property name="can_focus">False</property>
                                    <child>
                                      <object class="GtkEntry" id="exiimport_importdir_entry">
                                        <property name="visible">True</property>
                                        <property name="can_focus">True</property>
                                        <property name="tooltip_text" translatable="yes">Mountpoint of directory to import. Corresponds to %m in the gnome-volume-manager config dialog.</property>
                                        <property name="invisible_char">*</property>
                                      </object>
                                      <packing>
                                        <property name="expand">True</property>
                                        <property name="fill">True</property>
                                        <property name="position">0</property>
                                      </packing>
                                    </child>
                                    <child>
                                      <object class="GtkButton" id="button4">
                                        <property name="visible">True</property>
                                        <property name="can_focus">True</property>
                                        <property name="focus_on_click">False</property>
                                        <property name="receives_default">False</property>
                                        <signal name="clicked" handler="on_button_exiimport_browse_importdir_clicked" swapped="no"/>
                                        <child>
                                          <object class="GtkAlignment" id="alignment15">
                                            <property name="visible">True</property>
                                            <property name="can_focus">False</property>
                                            <property name="xscale">0</property>
                                            <property name="yscale">0</property>
                                            <child>
                                              <object class="GtkHBox" id="hbox19">
                                                <property name="visible">True</property>
                                                <property name="can_focus">False</property>
                                                <property name="spacing">2</property>
                                                <child>
                                                  <object class="GtkImage" id="image1">
                                                    <property name="visible">True</property>
                                                    <property name="can_focus">False</property>
                                                    <property name="stock">gtk-open</property>
                                                  </object>
                                                  <packing>
                                                    <property name="expand">False</property>
                                                    <property name="fill">False</property>
                                                    <property name="position">0</property>
                                                  </packing>
                                                </child>
                                                <child>
                                                  <object class="GtkLabel" id="label28">
                                                    <property name="visible">True</property>
                                                    <property name="can_focus">False</property>
                                                    <property name="label">Browse</property>
                                                    <property name="use_underline">True</property>
                                                  </object>
                                                  <packing>
                                                    <property name="expand">False</property>
                                                    <property name="fill">False</property>
                                                    <property name="position">1</property>
                                                  </packing>
                                                </child>
                                              </object>
                                            </child>
                                          </object>
                                        </child>
                                      </object>
                                      <packing>
                                        <property name="expand">False</property>
                                        <property name="fill">False</property>
                                        <property name="position">1</property>
                                      </packing>
                                    </child>
                                  </object>
                                </child>
                              </object>
                            </child>
                            <child type="label">
                              <object class="GtkLabel" id="label26">
                                <property name="visible">True</property>
                                <property name="can_focus">False</property>
                                <property name="label" translatable="yes">&lt;b&gt;Import directory&lt;/b&gt;</property>
                                <property name="use_markup">True</property>
                              </object>
                            </child>
                          </object>
                          <packing>
                            <property name="expand">True</property>
                            <property name="fill">True</property>
                            <property name="position">0</property>
                          </packing>
                        </child>
                        <child>
                          <object class="GtkFrame" id="frame14">
                            <property name="visible">True</property>
                            <property name="can_focus">False</property>
                            <property name="label_xalign">0</property>
                            <child>
                              <object class="GtkAlignment" id="alignment14">
                                <property name="visible">True</property>
                                <property name="can_focus">False</property>
                                <property name="left_padding">12</property>
                                <child>
                                  <object class="GtkHBox" id="hbox18">
                                    <property name="visible">True</property>
                                    <property name="can_focus">False</property>
                                    <child>
                                      <object class="GtkEntry" id="exiimport_targetdir_entry">
                                        <property name="visible">True</property>
                                        <property name="can_focus">True</property>
                                        <property name="tooltip_text" translatable="yes">Target directory. A subdirectory will be created in this directory.
</property>
                                        <property name="invisible_char">*</property>
                                      </object>
                                      <packing>
                                        <property name="expand">True</property>
                                        <property name="fill">True</property>
                                        <property name="position">0</property>
                                      </packing>
                                    </child>
                                    <child>
                                      <object class="GtkButton" id="button5">
                                        <property name="visible">True</property>
                                        <property name="can_focus">True</property>
                                        <property name="focus_on_click">False</property>
                                        <property name="receives_default">False</property>
                                        <signal name="clicked" handler="on_button_exiimport_browse_targetdir_clicked" swapped="no"/>
                                        <child>
                                          <object class="GtkAlignment" id="alignment16">
                                            <property name="visible">True</property>
                                            <property name="can_focus">False</property>
                                            <property name="xscale">0</property>
                                            <property name="yscale">0</property>
                                            <child>
                                              <object class="GtkHBox" id="hbox20">
                                                <property name="visible">True</property>
                                                <property name="can_focus">False</property>
                                                <property name="spacing">2</property>
                                                <child>
                                                  <object class="GtkImage" id="image2">
                                                    <property name="visible">True</property>
                                                    <property name="can_focus">False</property>
                                                    <property name="stock">gtk-open</property>
                                                  </object>
                                                  <packing>
                                                    <property name="expand">False</property>
                                                    <property name="fill">False</property>
                                                    <property name="position">0</property>
                                                  </packing>
                                                </child>
                                                <child>
                                                  <object class="GtkLabel" id="label29">
                                                    <property name="visible">True</property>
                                                    <property name="can_focus">False</property>
                                                    <property name="label">Browse</property>
                                                    <property name="use_underline">True</property>
                                                  </object>
                                                  <packing>
                                                    <property name="expand">False</property>
                                                    <property name="fill">False</property>
                                                    <property name="position">1</property>
                                                  </packing>
                                                </child>
                                              </object>
                                            </child>
                                          </object>
                                        </child>
                                      </object>
                                      <packing>
                                        <property name="expand">False</property>
                                        <property name="fill">False</property>
                                        <property name="position">1</property>
                                      </packing>
                                    </child>
                                  </object>
                                </child>
                              </object>
                            </child>
                            <child type="label">
                              <object class="GtkLabel" id="label27">
                                <property name="visible">True</property>
                                <property name="can_focus">False</property>
                                <property name="label" translatable="yes">&lt;b&gt;Target directory&lt;/b&gt;</property>
                                <property name="use_markup">True</property>
                              </object>
                            </child>
                          </object>
                          <packing>
                            <property name="expand">True</property>
                            <property name="fill">True</property>
                            <property name="position">2</property>
                          </packing>
                        </child>
                      </object>
                    </child>
                    <child type="tab">
                      <object class="GtkLabel" id="exiimport">
                        <property name="visible">True</property>
                        <property name="can_focus">False</property>
                        <property name="label" translatable="yes">exiimport</property>
                      </object>
                      <packing>
                        <property name="tab_fill">False</property>
                      </packing>
                    </child>
                    <child>
                      <object class="GtkVBox" id="vbox3">
                        <property name="visible">True</property>
                        <property name="can_focus">False</property>
                        <child>
                          <object class="GtkFrame" id="frame3">
                            <property name="width_request">120</property>
                            <property name="visible">True</property>
                            <property name="can_focus">False</property>
                            <property name="label_xalign">0</property>
                            <child>
                              <object class="GtkAlignment" id="alignment3">
                                <property name="visible">True</property>
                                <property name="can_focus">False</property>
                                <property name="left_padding">12</property>
                                <child>
                                  <object class="GtkHBox" id="hbox3">
                                    <property name="visible">True</property>
                                    <property name="can_focus">False</property>
                                    <child>
                                      <object class="GtkRadioButton" id="exirename_cam_id_entry_button_auto">
                                        <property name="label" translatable="yes">Automatic</property>
                                        <property name="visible">True</property>
                                        <property name="can_focus">True</property>
                                        <property name="receives_default">False</property>
                                        <property name="tooltip_text" translatable="yes">Automatically determined by looking for a section in your INI file that matches the model tag of the EXIF information.</property>
                                        <property name="use_underline">True</property>
                                        <property name="active">True</property>
                                        <property name="draw_indicator">True</property>
                                        <signal name="clicked" handler="on_exirename_camid_auto_activate" swapped="no"/>
                                      </object>
                                      <packing>
                                        <property name="expand">False</property>
                                        <property name="fill">False</property>
                                        <property name="position">0</property>
                                      </packing>
                                    </child>
                                    <child>
                                      <object class="GtkRadioButton" id="exirename_cam_id_entry_button_custom">
                                        <property name="label" translatable="yes">Custom value:</property>
                                        <property name="visible">True</property>
                                        <property name="can_focus">True</property>
                                        <property name="receives_default">False</property>
                                        <property name="tooltip_text" translatable="yes">Choose a fixed string of 3 characters.</property>
                                        <property name="use_underline">True</property>
                                        <property name="draw_indicator">True</property>
                                        <property name="group">exirename_cam_id_entry_button_auto</property>
                                        <signal name="clicked" handler="on_exirename_camid_custom_activate" swapped="no"/>
                                      </object>
                                      <packing>
                                        <property name="expand">False</property>
                                        <property name="fill">False</property>
                                        <property name="position">1</property>
                                      </packing>
                                    </child>
                                    <child>
                                      <object class="GtkEntry" id="exirename_cam_id_entry">
                                        <property name="visible">True</property>
                                        <property name="sensitive">False</property>
                                        <property name="can_focus">True</property>
                                        <property name="max_length">3</property>
                                        <property name="invisible_char">*</property>
                                        <property name="width_chars">3</property>
                                      </object>
                                      <packing>
                                        <property name="expand">True</property>
                                        <property name="fill">True</property>
                                        <property name="position">2</property>
                                      </packing>
                                    </child>
                                  </object>
                                </child>
                              </object>
                            </child>
                            <child type="label">
                              <object class="GtkLabel" id="label14">
                                <property name="visible">True</property>
                                <property name="can_focus">False</property>
                                <property name="label" translatable="yes">&lt;b&gt;Camera ID&lt;/b&gt;</property>
                                <property name="use_markup">True</property>
                              </object>
                            </child>
                          </object>
                          <packing>
                            <property name="expand">True</property>
                            <property name="fill">True</property>
                            <property name="position">0</property>
                          </packing>
                        </child>
                        <child>
                          <object class="GtkFrame" id="frame4">
                            <property name="visible">True</property>
                            <property name="can_focus">False</property>
                            <property name="label_xalign">0</property>
                            <child>
                              <object class="GtkAlignment" id="alignment4">
                                <property name="visible">True</property>
                                <property name="can_focus">False</property>
                                <property name="left_padding">12</property>
                                <child>
                                  <object class="GtkHBox" id="hbox4">
                                    <property name="visible">True</property>
                                    <property name="can_focus">False</property>
                                    <child>
                                      <object class="GtkRadioButton" id="exirename_artist_initials_entry_button_auto">
                                        <property name="label" translatable="yes">Automatic</property>
                                        <property name="visible">True</property>
                                        <property name="can_focus">True</property>
                                        <property name="receives_default">False</property>
                                        <property name="tooltip_text" translatable="yes">Automatically determined by looking for a section in your INI file that matches the model tag of the EXIF information.</property>
                                        <property name="use_underline">True</property>
                                        <property name="active">True</property>
                                        <property name="draw_indicator">True</property>
                                        <signal name="clicked" handler="on_exirename_artist_auto_activate" swapped="no"/>
                                      </object>
                                      <packing>
                                        <property name="expand">False</property>
                                        <property name="fill">False</property>
                                        <property name="position">0</property>
                                      </packing>
                                    </child>
                                    <child>
                                      <object class="GtkRadioButton" id="exirename_artist_initials_entry_button_custom">
                                        <property name="label" translatable="yes">Custom value:</property>
                                        <property name="visible">True</property>
                                        <property name="can_focus">True</property>
                                        <property name="receives_default">False</property>
                                        <property name="tooltip_text" translatable="yes">Choose a fixed string of 2 characters.</property>
                                        <property name="use_underline">True</property>
                                        <property name="draw_indicator">True</property>
                                        <property name="group">exirename_artist_initials_entry_button_auto</property>
                                        <signal name="clicked" handler="on_exirename_artist_custom_activate" swapped="no"/>
                                      </object>
                                      <packing>
                                        <property name="expand">False</property>
                                        <property name="fill">False</property>
                                        <property name="position">1</property>
                                      </packing>
                                    </child>
                                    <child>
                                      <object class="GtkEntry" id="exirename_artist_initials_entry">
                                        <property name="visible">True</property>
                                        <property name="sensitive">False</property>
                                        <property name="can_focus">True</property>
                                        <property name="max_length">2</property>
                                        <property name="invisible_char">*</property>
                                        <property name="width_chars">2</property>
                                      </object>
                                      <packing>
                                        <property name="expand">True</property>
                                        <property name="fill">True</property>
                                        <property name="position">2</property>
                                      </packing>
                                    </child>
                                  </object>
                                </child>
                              </object>
                            </child>
                            <child type="label">
                              <object class="GtkLabel" id="label15">
                                <property name="visible">True</property>
                                <property name="can_focus">False</property>
                                <property name="label" translatable="yes">&lt;b&gt;Artist initials&lt;/b&gt;</property>
                                <property name="use_markup">True</property>
                              </object>
                            </child>
                          </object>
                          <packing>
                            <property name="expand">True</property>
                            <property name="fill">True</property>
                            <property name="position">1</property>
                          </packing>
                        </child>
                        <child>
                          <object class="GtkFrame" id="frame16">
                            <property name="width_request">120</property>
                            <property name="visible">True</property>
                            <property name="can_focus">False</property>
                            <property name="label_xalign">0</property>
                            <child>
                              <object class="GtkAlignment" id="alignment18">
                                <property name="visible">True</property>
                                <property name="can_focus">False</property>
                                <property name="left_padding">12</property>
                                <child>
                                  <object class="GtkVBox" id="vbox14">
                                    <property name="visible">True</property>
                                    <property name="can_focus">False</property>
                                    <child>
                                      <object class="GtkCheckButton" id="exirename_include_timestamp_checkbutton">
                                        <property name="label" translatable="yes">include timestamp in filename</property>
                                        <property name="visible">True</property>
                                        <property name="can_focus">True</property>
                                        <property name="receives_default">False</property>
                                        <property name="tooltip_text" translatable="yes">Create filenames containing the image time, for example 20071231-235959-n001234-xy000.jpg instead of 
20071231-n001234-xy000.jpg .</property>
                                        <property name="use_underline">True</property>
                                        <property name="draw_indicator">True</property>
                                        <signal name="clicked" handler="on_exirename_include_timestamp_checkbutton_clicked" swapped="no"/>
                                      </object>
                                      <packing>
                                        <property name="expand">False</property>
                                        <property name="fill">False</property>
                                        <property name="position">0</property>
                                      </packing>
                                    </child>
                                  </object>
                                </child>
                              </object>
                            </child>
                            <child type="label">
                              <object class="GtkLabel" id="label32">
                                <property name="visible">True</property>
                                <property name="can_focus">False</property>
                                <property name="label" translatable="yes">Options</property>
                                <property name="use_markup">True</property>
                              </object>
                            </child>
                          </object>
                          <packing>
                            <property name="expand">True</property>
                            <property name="fill">True</property>
                            <property name="position">2</property>
                          </packing>
                        </child>
                      </object>
                      <packing>
                        <property name="position">1</property>
                      </packing>
                    </child>
                    <child type="tab">
                      <object class="GtkLabel" id="exirename">
                        <property name="visible">True</property>
                        <property name="can_focus">False</property>
                        <property name="label" translatable="yes">exirename</property>
                      </object>
                      <packing>
                        <property name="position">1</property>
                        <property name="tab_fill">False</property>
                      </packing>
                    </child>
                    <child>
                      <object class="GtkFrame" id="frame8">
                        <property name="width_request">120</property>
                        <property name="visible">True</property>
                        <property name="can_focus">False</property>
                        <property name="label_xalign">0</property>
                        <child>
                          <object class="GtkAlignment" id="alignment9">
                            <property name="visible">True</property>
                            <property name="can_focus">False</property>
                            <property name="left_padding">12</property>
                            <child>
                              <object class="GtkHBox" id="hbox8">
                                <property name="visible">True</property>
                                <property name="can_focus">False</property>
                                <child>
                                  <object class="GtkRadioButton" id="exiperson_section_entry_button_auto">
                                    <property name="label" translatable="yes">Automatic</property>
                                    <property name="visible">True</property>
                                    <property name="can_focus">True</property>
                                    <property name="receives_default">False</property>
                                    <property name="tooltip_text" translatable="yes">Automatically determined by looking for a section in your INI file that matches the model tag of the EXIF information.</property>
                                    <property name="use_underline">True</property>
                                    <property name="active">True</property>
                                    <property name="draw_indicator">True</property>
                                    <signal name="clicked" handler="on_exiperson_section_auto_activate" swapped="no"/>
                                  </object>
                                  <packing>
                                    <property name="expand">False</property>
                                    <property name="fill">False</property>
                                    <property name="position">0</property>
                                  </packing>
                                </child>
                                <child>
                                  <object class="GtkRadioButton" id="exiperson_section_entry_button_custom">
                                    <property name="label" translatable="yes">Custom value:</property>
                                    <property name="visible">True</property>
                                    <property name="can_focus">True</property>
                                    <property name="receives_default">False</property>
                                    <property name="tooltip_text" translatable="yes">Choose an other section in exif.conf.</property>
                                    <property name="use_underline">True</property>
                                    <property name="draw_indicator">True</property>
                                    <property name="group">exiperson_section_entry_button_auto</property>
                                    <signal name="clicked" handler="on_exiperson_section_custom_activate" swapped="no"/>
                                  </object>
                                  <packing>
                                    <property name="expand">False</property>
                                    <property name="fill">False</property>
                                    <property name="position">1</property>
                                  </packing>
                                </child>
                                <child>
                                  <object class="GtkEntry" id="exiperson_section_entry">
                                    <property name="visible">True</property>
                                    <property name="sensitive">False</property>
                                    <property name="can_focus">True</property>
                                    <property name="invisible_char">*</property>
                                    <property name="width_chars">30</property>
                                  </object>
                                  <packing>
                                    <property name="expand">True</property>
                                    <property name="fill">True</property>
                                    <property name="position">2</property>
                                  </packing>
                                </child>
                              </object>
                            </child>
                          </object>
                        </child>
                        <child type="label">
                          <object class="GtkLabel" id="label19">
                            <property name="visible">True</property>
                            <property name="can_focus">False</property>
                            <property name="label" translatable="yes">&lt;b&gt;EXIF settings section&lt;/b&gt;</property>
                            <property name="use_markup">True</property>
                          </object>
                        </child>
                      </object>
                      <packing>
                        <property name="position">2</property>
                      </packing>
                    </child>
                    <child type="tab">
                      <object class="GtkLabel" id="exiperson">
                        <property name="visible">True</property>
                        <property name="can_focus">False</property>
                        <property name="label" translatable="yes">exiperson</property>
                      </object>
                      <packing>
                        <property name="position">2</property>
                        <property name="tab_fill">False</property>
                      </packing>
                    </child>
                    <child>
                      <object class="GtkFrame" id="frame15">
                        <property name="width_request">120</property>
                        <property name="visible">True</property>
                        <property name="can_focus">False</property>
                        <property name="label_xalign">0</property>
                        <child>
                          <object class="GtkAlignment" id="alignment17">
                            <property name="visible">True</property>
                            <property name="can_focus">False</property>
                            <property name="left_padding">12</property>
                            <child>
                              <object class="GtkVBox" id="vbox13">
                                <property name="visible">True</property>
                                <property name="can_focus">False</property>
                                <child>
                                  <object class="GtkCheckButton" id="exiconvert_remove_lqjpeg_checkbutton">
                                    <property name="label" translatable="yes">remove low quality version (...00l.jpg)</property>
                                    <property name="visible">True</property>
                                    <property name="can_focus">True</property>
                                    <property name="receives_default">False</property>
                                    <property name="tooltip_text" translatable="yes">Force update even if EXIF is already present. The fields handled by thes scripts are kept anyway.</property>
                                    <property name="use_underline">True</property>
                                    <property name="draw_indicator">True</property>
                                    <signal name="clicked" handler="on_exiconvert_remove_lqjpeg_checkbutton_clicked" swapped="no"/>
                                  </object>
                                  <packing>
                                    <property name="expand">False</property>
                                    <property name="fill">False</property>
                                    <property name="position">0</property>
                                  </packing>
                                </child>
                              </object>
                            </child>
                          </object>
                        </child>
                        <child type="label">
                          <object class="GtkLabel" id="label31">
                            <property name="visible">True</property>
                            <property name="can_focus">False</property>
                            <property name="label" translatable="yes">Options</property>
                            <property name="use_markup">True</property>
                          </object>
                        </child>
                      </object>
                      <packing>
                        <property name="position">3</property>
                      </packing>
                    </child>
                    <child type="tab">
                      <object class="GtkLabel" id="exiconvert">
                        <property name="visible">True</property>
                        <property name="can_focus">False</property>
                        <property name="label" translatable="yes">exiconvert</property>
                      </object>
                      <packing>
                        <property name="position">3</property>
                        <property name="tab_fill">False</property>
                      </packing>
                    </child>
                    <child>
                      <object class="GtkFrame" id="frame7">
                        <property name="width_request">120</property>
                        <property name="visible">True</property>
                        <property name="can_focus">False</property>
                        <property name="label_xalign">0</property>
                        <child>
                          <object class="GtkAlignment" id="alignment8">
                            <property name="visible">True</property>
                            <property name="can_focus">False</property>
                            <property name="left_padding">12</property>
                            <child>
                              <object class="GtkCheckButton" id="exiassign_force_checkbutton">
                                <property name="label" translatable="yes">force update</property>
                                <property name="visible">True</property>
                                <property name="can_focus">True</property>
                                <property name="receives_default">False</property>
                                <property name="tooltip_text" translatable="yes">Force update even if EXIF is already present. The fields handled by thes scripts are kept anyway.</property>
                                <property name="use_underline">True</property>
                                <property name="draw_indicator">True</property>
                                <signal name="clicked" handler="on_exiassign_force_checkbutton_clicked" swapped="no"/>
                              </object>
                            </child>
                          </object>
                        </child>
                        <child type="label">
                          <object class="GtkLabel" id="label18">
                            <property name="visible">True</property>
                            <property name="can_focus">False</property>
                            <property name="label" translatable="yes">Options</property>
                            <property name="use_markup">True</property>
                          </object>
                        </child>
                      </object>
                      <packing>
                        <property name="position">4</property>
                      </packing>
                    </child>
                    <child type="tab">
                      <object class="GtkLabel" id="exiassign">
                        <property name="visible">True</property>
                        <property name="can_focus">False</property>
                        <property name="label" translatable="yes">exiassign</property>
                      </object>
                      <packing>
                        <property name="position">4</property>
                        <property name="tab_fill">False</property>
                      </packing>
                    </child>
                    <child>
                      <object class="GtkFrame" id="frame9">
                        <property name="width_request">120</property>
                        <property name="visible">True</property>
                        <property name="can_focus">False</property>
                        <property name="label_xalign">0</property>
                        <child>
                          <object class="GtkVBox" id="vbox10">
                            <property name="visible">True</property>
                            <property name="can_focus">False</property>
                            <child>
                              <object class="GtkRadioButton" id="exigate_nooptions">
                                <property name="label" translatable="yes">None</property>
                                <property name="visible">True</property>
                                <property name="can_focus">True</property>
                                <property name="receives_default">False</property>
                                <property name="tooltip_text" translatable="yes">no options</property>
                                <property name="use_underline">True</property>
                                <property name="draw_indicator">True</property>
                              </object>
                              <packing>
                                <property name="expand">False</property>
                                <property name="fill">False</property>
                                <property name="position">0</property>
                              </packing>
                            </child>
                            <child>
                              <object class="GtkRadioButton" id="exigate_cleanup">
                                <property name="label" translatable="yes">Cleanup</property>
                                <property name="visible">True</property>
                                <property name="can_focus">True</property>
                                <property name="receives_default">False</property>
                                <property name="tooltip_text" translatable="yes">The opposite of --additional-fields, that is, remove additional fields from gthumb comments.</property>
                                <property name="use_underline">True</property>
                                <property name="active">True</property>
                                <property name="draw_indicator">True</property>
                                <property name="group">exigate_nooptions</property>
                                <signal name="clicked" handler="on_exigate_cleanup_activate" swapped="no"/>
                              </object>
                              <packing>
                                <property name="expand">False</property>
                                <property name="fill">False</property>
                                <property name="position">1</property>
                              </packing>
                            </child>
                            <child>
                              <object class="GtkRadioButton" id="exigate_addfields">
                                <property name="label" translatable="yes">Additional Fields</property>
                                <property name="visible">True</property>
                                <property name="can_focus">True</property>
                                <property name="receives_default">False</property>
                                <property name="tooltip_text" translatable="yes">When gating from Exif to gthumb, combine additional Exif fields into the comment.</property>
                                <property name="use_underline">True</property>
                                <property name="draw_indicator">True</property>
                                <property name="group">exigate_nooptions</property>
                                <signal name="clicked" handler="on_exigate_addfields_activate" swapped="no"/>
                              </object>
                              <packing>
                                <property name="expand">False</property>
                                <property name="fill">False</property>
                                <property name="position">2</property>
                              </packing>
                            </child>
                            <child>
                              <object class="GtkRadioButton" id="exigate_template">
                                <property name="label" translatable="yes">Additional Fields and Templates</property>
                                <property name="visible">True</property>
                                <property name="can_focus">True</property>
                                <property name="receives_default">False</property>
                                <property name="tooltip_text" translatable="yes">Like --additional-fields, but also combine empty fields as templates into the comment.</property>
                                <property name="use_underline">True</property>
                                <property name="draw_indicator">True</property>
                                <property name="group">exigate_nooptions</property>
                                <signal name="clicked" handler="on_exigate_template_activate" swapped="no"/>
                              </object>
                              <packing>
                                <property name="expand">False</property>
                                <property name="fill">False</property>
                                <property name="position">3</property>
                              </packing>
                            </child>
                          </object>
                        </child>
                        <child type="label">
                          <object class="GtkLabel" id="label21">
                            <property name="visible">True</property>
                            <property name="can_focus">False</property>
                            <property name="label" translatable="yes">&lt;b&gt;Options&lt;/b&gt;</property>
                            <property name="use_markup">True</property>
                          </object>
                        </child>
                      </object>
                      <packing>
                        <property name="position">5</property>
                      </packing>
                    </child>
                    <child type="tab">
                      <object class="GtkLabel" id="exigate">
                        <property name="visible">True</property>
                        <property name="can_focus">False</property>
                        <property name="label" translatable="yes">exigate</property>
                      </object>
                      <packing>
                        <property name="position">5</property>
                        <property name="tab_fill">False</property>
                      </packing>
                    </child>
                  </object>
                  <packing>
                    <property name="expand">False</property>
                    <property name="fill">True</property>
                    <property name="position">0</property>
                  </packing>
                </child>
                <child>
                  <object class="GtkFrame" id="frame5">
                    <property name="visible">True</property>
                    <property name="can_focus">False</property>
                    <property name="label_xalign">0</property>
                    <child>
                      <object class="GtkAlignment" id="alignment5">
                        <property name="visible">True</property>
                        <property name="can_focus">False</property>
                        <property name="left_padding">12</property>
                        <child>
                          <object class="GtkHBox" id="hbox13">
                            <property name="visible">True</property>
                            <property name="can_focus">False</property>
                            <child>
                              <object class="GtkProgressBar" id="progressbar1">
                                <property name="visible">True</property>
                                <property name="can_focus">False</property>
                                <property name="pulse_step">0.10000000149</property>
                              </object>
                              <packing>
                                <property name="expand">True</property>
                                <property name="fill">True</property>
                                <property name="position">0</property>
                              </packing>
                            </child>
                            <child>
                              <object class="GtkButton" id="cancel_button">
                                <property name="label">gtk-cancel</property>
                                <property name="visible">True</property>
                                <property name="sensitive">False</property>
                                <property name="can_focus">True</property>
                                <property name="can_default">True</property>
                                <property name="receives_default">False</property>
                                <property name="use_stock">True</property>
                                <signal name="clicked" handler="on_cancel_activate" swapped="no"/>
                              </object>
                              <packing>
                                <property name="expand">False</property>
                                <property name="fill">False</property>
                                <property name="padding">10</property>
                                <property name="position">1</property>
                              </packing>
                            </child>
                            <child>
                              <object class="GtkButton" id="activate_button">
                                <property name="label">gtk-apply</property>
                                <property name="visible">True</property>
                                <property name="can_focus">True</property>
                                <property name="can_default">True</property>
                                <property name="receives_default">False</property>
                                <property name="use_stock">True</property>
                                <signal name="clicked" handler="on_run_activate" swapped="no"/>
                              </object>
                              <packing>
                                <property name="expand">False</property>
                                <property name="fill">False</property>
                                <property name="padding">10</property>
                                <property name="position">2</property>
                              </packing>
                            </child>
                          </object>
                        </child>
                      </object>
                    </child>
                    <child type="label">
                      <object class="GtkLabel" id="label16">
                        <property name="visible">True</property>
                        <property name="can_focus">False</property>
                        <property name="label" translatable="yes">Progress</property>
                        <property name="use_markup">True</property>
                      </object>
                    </child>
                  </object>
                  <packing>
                    <property name="expand">False</property>
                    <property name="fill">True</property>
                    <property name="position">1</property>
                  </packing>
                </child>
                <child>
                  <object class="GtkHSeparator" id="hseparator2">
                    <property name="visible">True</property>
                    <property name="can_focus">False</property>
                  </object>
                  <packing>
                    <property name="expand">False</property>
                    <property name="fill">True</property>
                    <property name="position">2</property>
                  </packing>
                </child>
                <child>
                  <object class="GtkFrame" id="frame6">
                    <property name="visible">True</property>
                    <property name="can_focus">False</property>
                    <property name="label_xalign">0</property>
                    <property name="shadow_type">none</property>
                    <child>
                      <object class="GtkAlignment" id="alignment6">
                        <property name="visible">True</property>
                        <property name="can_focus">False</property>
                        <property name="left_padding">12</property>
                        <child>
                          <object class="GtkScrolledWindow" id="scrolledwindow2">
                            <property name="visible">True</property>
                            <property name="can_focus">True</property>
                            <property name="shadow_type">in</property>
                            <child>
                              <object class="GtkTextView" id="textview1">
                                <property name="visible">True</property>
                                <property name="can_focus">True</property>
                                <property name="editable">False</property>
                              </object>
                            </child>
                          </object>
                        </child>
                      </object>
                    </child>
                    <child type="label">
                      <object class="GtkLabel" id="label17">
                        <property name="visible">True</property>
                        <property name="can_focus">False</property>
                        <property name="label" translatable="yes">Console</property>
                        <property name="use_markup">True</property>
                      </object>
                    </child>
                  </object>
                  <packing>
                    <property name="expand">True</property>
                    <property name="fill">True</property>
                    <property name="position">3</property>
                  </packing>
                </child>
              </object>
              <packing>
                <property name="resize">True</property>
                <property name="shrink">True</property>
              </packing>
            </child>
          </object>
          <packing>
            <property name="expand">True</property>
            <property name="fill">True</property>
            <property name="position">1</property>
          </packing>
        </child>
      </object>
    </child>
  </object>
</interface>
