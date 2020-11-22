from Screens.Screen import Screen
from Components.ConfigList import ConfigListScreen
from Components.config import config, getConfigListEntry
from Components.Label import Label
from Components.Sources.StaticText import StaticText

class HdmiCECSetupScreen(Screen, ConfigListScreen):
	skin = ["""
	<screen position="center,center" size="%d,%d" title="HDMI-CEC setup">
		<widget name="config" position="%d,%d" size="%d,%d" font="Regular;%d" itemHeight="%d" scrollbarMode="showOnDemand" valign="center"/>
		<widget name="description" position="%d,%d" size="%d,%d" zPosition="10" font="Regular;%d" halign="center" valign="center" />
		<widget source="current_address" render="Label" position="%d,%d" size="%d,%d" zPosition="10" font="Regular;%d" halign="left" valign="center" />
		<widget source="fixed_address" render="Label" position="%d,%d" size="%d,%d" zPosition="10" font="Regular;%d" halign="left" valign="center" />
		<ePixmap pixmap="buttons/red.png" position="%d,e-%d" size="%d,%d" alphatest="on" scale="1"/>
		<ePixmap pixmap="buttons/green.png" position="%d,e-%d" size="%d,%d" alphatest="on" scale="1"/>
		<ePixmap pixmap="buttons/yellow.png" position="%d,e-%d" size="%d,%d" alphatest="on" scale="1"/>
		<ePixmap pixmap="buttons/blue.png" position="%d,e-%d" size="%d,%d" alphatest="on" scale="1"/>
		<widget source="key_red" render="Label" position="%d,e-%d" zPosition="1" size="%d,%d" font="Regular;%d" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />
		<widget source="key_green" render="Label" position="%d,e-%d" zPosition="1" size="%d,%d" font="Regular;%d" halign="center" valign="center" backgroundColor="#1f771f" transparent="1" />
		<widget source="key_yellow" render="Label" position="%d,e-%d" zPosition="1" size="%d,%d" font="Regular;%d" halign="center" valign="center" backgroundColor="#a08500" transparent="1" />
		<widget source="key_blue" render="Label" position="%d,e-%d" zPosition="1" size="%d,%d" font="Regular;%d" halign="center" valign="center" backgroundColor="#18188b" transparent="1" />
	</screen>""",
		600, 500,                 # screen
		25, 25, 550, 250, 20, 25, # config
		25, 275, 550, 100, 21,    # description
		25, 375, 550, 30, 21,     # current_address
		25, 405, 550, 30, 21,     # fixed_address
		20, 45, 140, 40,          # red graphic
		160, 45, 140, 40,         # green graphic
		300, 45, 140, 40,         # yellow graphic
		440, 45, 140, 40,         # blue graphic
		20, 45, 140, 40, 20,      # red text
		160, 45, 140, 40, 20,     # green text
		300, 45, 140, 40, 20,     # yellow text
		440, 45, 140, 40, 20,     # blue text
		]
		
	def __init__(self, session):
		self.skin = HdmiCECSetupScreen.skin
		Screen.__init__(self, session)

		self.setTitle(_("HDMI-CEC setup"))

		from Components.ActionMap import ActionMap
		from Components.Button import Button

		self["key_red"] = StaticText(_("Cancel"))
		self["key_green"] = StaticText(_("OK"))
		self["key_yellow"] = StaticText(_("Set fixed"))
		self["key_blue"] = StaticText(_("Clear fixed"))
		self["current_address"] = StaticText()
		self["fixed_address"] = StaticText()
		self["description"] = Label("")

		self["actions"] = ActionMap(["SetupActions", "ColorActions", "MenuActions"],
		{
			"ok": self.keyOk,
			"save": self.keyGo,
			"cancel": self.keyCancel,
			"green": self.keyGo,
			"red": self.keyCancel,
			"yellow": self.setFixedAddress,
			"blue": self.clearFixedAddress,
			"menu": self.closeRecursive,
		}, -2)

		self.list = []
		self.logpath_entry = None
		ConfigListScreen.__init__(self, self.list, session = self.session)
		self.createSetup()
		self.updateAddress()
		
		if not self.selectionChanged in self["config"].onSelectionChanged:
			self["config"].onSelectionChanged.append(self.selectionChanged)
		self.selectionChanged()

	def selectionChanged(self):
		self["description"].setText(self.getCurrentDescription())

	def createSetup(self):
		self.list = []
		self.list.append(getConfigListEntry(_("Enabled"), config.hdmicec.enabled, _("Hint text: Enabled")))
		if config.hdmicec.enabled.value:
			self.list.append(getConfigListEntry(_("Put TV in standby"), config.hdmicec.control_tv_standby, _("Hint text: Put TV in standby")))
			self.list.append(getConfigListEntry(_("Wakeup TV from standby"), config.hdmicec.control_tv_wakeup, _("Hint text: Wakeup TV from standby")))
			if config.hdmicec.control_tv_wakeup.value:
				self.list.append(getConfigListEntry(_("Wakeup command for TV"), config.hdmicec.tv_wakeup_command, _("Hint text: Wakeup command for TV")))
			self.list.append(getConfigListEntry(_("Regard deep standby as standby"), config.hdmicec.handle_deepstandby_events, _("Hint text: Regard deep standby as standby")))
			self.list.append(getConfigListEntry(_("Switch TV to correct input"), config.hdmicec.report_active_source, _("Hint text: Switch TV to correct input")))
			self.list.append(getConfigListEntry(_("Use TV remote control"), config.hdmicec.report_active_menu, _("Hint text: Use TV remote control")))
			self.list.append(getConfigListEntry(_("Handle standby from TV"), config.hdmicec.handle_tv_standby, _("Hint text: Handle standby from TV")))
			self.list.append(getConfigListEntry(_("Handle wakeup from TV"), config.hdmicec.handle_tv_wakeup,_("Hint text: Handle wakeup from TV")))
			if config.hdmicec.handle_tv_wakeup.value:
				self.list.append(getConfigListEntry(_("Wakeup signal from TV"), config.hdmicec.tv_wakeup_detection, _("Hint text: Wakeup signal from TV")))
			self.list.append(getConfigListEntry(_("Forward volume keys"), config.hdmicec.volume_forwarding, _("Hint text: Forward volume keys")))
			self.list.append(getConfigListEntry(_("Put receiver in standby"), config.hdmicec.control_receiver_standby, _("Hint text: Put receiver in standby")))
			self.list.append(getConfigListEntry(_("Wakeup receiver from standby"), config.hdmicec.control_receiver_wakeup, _("Hint text: Wakeup receiver from standby")))
			self.list.append(getConfigListEntry(_("Minimum send interval"), config.hdmicec.minimum_send_interval, _("Hint text: Minimum send interval")))
			self.list.append(getConfigListEntry(_("Repeat leave standby messages"), config.hdmicec.repeat_wakeup_timer, _("Hint text: Repeat leave standby messages")))
			self.list.append(getConfigListEntry(_("Send 'sourceactive' before zap timers"), config.hdmicec.sourceactive_zaptimers, _("Hint text: Send 'sourceactive' before zap timers")))
			self.list.append(getConfigListEntry(_("Detect next boxes before standby"), config.hdmicec.next_boxes_detect, _("Hint text: Detect next boxes before standby")))
			self.list.append(getConfigListEntry(_("Debug to file"), config.hdmicec.debug, _("Hint text: Debug to file")))
			self.logpath_entry = getConfigListEntry(_("Select path for logfile"), config.hdmicec.log_path, _("Hint text: Select path for logfile"))
			if config.hdmicec.debug.value != "0":
				self.list.append(self.logpath_entry)
		self["config"].list = self.list
		self["config"].l.setList(self.list)

	def keyLeft(self):
		ConfigListScreen.keyLeft(self)
		self.createSetup()

	def keyRight(self):
		ConfigListScreen.keyRight(self)
		self.createSetup()

	def keyGo(self):
		for x in self["config"].list:
			x[1].save()
		self.close()

	def keyCancel(self):
		for x in self["config"].list:
			x[1].cancel()
		self.close()

	def keyOk(self):
		currentry = self["config"].getCurrent()
		if currentry == self.logpath_entry:
			self.set_path()
		else:
			self.keyGo()

	def setFixedAddress(self):
		import Components.HdmiCec
		Components.HdmiCec.hdmi_cec.setFixedPhysicalAddress(Components.HdmiCec.hdmi_cec.getPhysicalAddress())
		self.updateAddress()

	def clearFixedAddress(self):
		import Components.HdmiCec
		Components.HdmiCec.hdmi_cec.setFixedPhysicalAddress("0.0.0.0")
		self.updateAddress()

	def updateAddress(self):
		import Components.HdmiCec
		self["current_address"].setText(_("Current CEC address") + ": " + Components.HdmiCec.hdmi_cec.getPhysicalAddress())
		if config.hdmicec.fixed_physical_address.value == "0.0.0.0":
			fixedaddresslabel = ""
		else:
			fixedaddresslabel = _("Using fixed address") + ": " + config.hdmicec.fixed_physical_address.value
		self["fixed_address"].setText(fixedaddresslabel)

	def logPath(self, res):
		if res is not None:
			config.hdmicec.log_path.value = res

	def set_path(self):
		inhibitDirs = ["/autofs", "/bin", "/boot", "/dev", "/etc", "/lib", "/proc", "/sbin", "/sys", "/tmp", "/usr"]
		from Screens.LocationBox import LocationBox
		txt = _("Select directory for logfile")
		self.session.openWithCallback(self.logPath, LocationBox, text=txt, currDir=config.hdmicec.log_path.value,
				bookmarks=config.hdmicec.bookmarks, autoAdd=False, editDir=True,
				inhibitDirs=inhibitDirs, minFree=1
				)

def main(session, **kwargs):
	session.open(HdmiCECSetupScreen)

def startSetup(menuid):
	# only show in the menu when set to intermediate or higher
	if menuid == "video" and config.av.videoport.value == "DVI" and config.usage.setup_level.index >= 1:
		return [(_("HDMI-CEC setup"), main, "hdmi_cec_setup", 0)]
	return []

def Plugins(**kwargs):
	from os import path
	if path.exists("/dev/hdmi_cec") or path.exists("/dev/misc/hdmi_cec0"):
		import Components.HdmiCec
		from Plugins.Plugin import PluginDescriptor
		return [PluginDescriptor(where = PluginDescriptor.WHERE_MENU, fnc = startSetup)]
	return []
