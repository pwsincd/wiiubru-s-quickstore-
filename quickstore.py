#! /usr/bin/python
# Version 1
# creates the json directory for wiiubru's quick web interface(by default)

import os, json, zipfile, imghdr, traceback, sys, ast
from pprint import pformat
import xml.etree.ElementTree as ET

print "Content-type: text/html\n\n"

def cgiprint(inp):
	# print and flush, to update web right away
	print(inp)
	sys.stdout.flush()

# try and catch ANY error so web has output
try:

	# list of featured apps, these will be moved to the top of the json file
	featured = ["asturoids", "spacegame", "flappy_bird", "homebrew_launcher", "loadiine_gx2", "retro_launcher", "pong", "pacman", "snake", "mgba_libretro", "snes9x2010_libretro",  "gambatte_libretro", "CHIP8", "quicknes_libretro", "mame2003_libretro", "genesis_plus_gx_libretro", "appstore", "cfwbooter", "mocha", "haxchi", "hidtovpad", "geckiine", "wuphax", "saviine", "ftpiiu", "wudump", "u-paint", "cbhc", "hid_keyboard_monitor", "LiveSynthesisU", "keyboard_example"]


	# This function parses out several attributes from xml
	def xml_read(incoming, tree, app):
		try:
			outgoing = []
			for key in incoming:
				try:
					outgoing.append(tree.find(key).text)
				except:
					cgiprint("%s: Missing &lt;%s&gt; in meta.xml<br>" % (app, key))
					outgoing.append("N/A")
			return tuple(outgoing)
		except:
			return False

	# the resulting json output
	out = []

	
	apps = os.listdir("apps")

	for app in apps:
		# ignore dotfiles
		if app.startswith("."):
			continue

		targdir = "apps"

		# get meta.xml file from HBL
		xmlfile = targdir + "/%s/meta.xml" % app

		# get icon.png file from HBL
		iconfile = targdir + "/%s/icon.png" % app

		if not os.path.exists(iconfile) or imghdr.what(iconfile) != "png":
			cgiprint("Skipping %s as its icon.png isn't a png file or doesn't exist<br>" % app)
			continue

		# create some default fields
		name = coder = desc = long_desc = version = source = updated = filesize = category = src_link = "N/A"
		typee = "elf"

		# find a binary in this app folder
		binary = None
		for file in os.listdir(targdir + "/%s" % app):
			if file.endswith(".elf") or file.endswith(".rpx"):
				binary = file

		# if there's no binary found, continue
		if not binary:
			continue

		# make sure rpxes are categorized as such
		if binary.endswith(".rpx"):
			typee = "rpx"

		# get fields out of xml
		if os.path.isfile(xmlfile):
			# parse the xml file
			tree = ET.parse(xmlfile)

			# pull out those attributes
			resp = xml_read(["name", "coder", "short_description", "url", "long_description", "version", "category"], tree, app)
			
			# skip app if invalid response from meta parsing
			if not resp:
				cgiprint("Error in meta.xml for %s, skipping...<br>" % app)
				continue
				
			# set attributes
			name, coder, desc, source, long_desc, version, category = resp

		# sanitize long_desc for json output
		long_desc = long_desc.replace("\n", "\\n").replace("\t", "\\t")

		# get icon path
		icon = targdir + "/%s/icon.png" % app

		# append to output json
		#out.append({"version": version, "directory": app, "name": name, "author": coder, "desc": desc, "url": source, "binary": binary, "long_desc": long_desc, "type": typee, "cat": category})
		out.append({"long_desc": long_desc, "version": version, "directory": app, "name": name, "binary": binary, "cat": category})

	# json string formatting
	jsonstring = json.dumps(out, indent=4, separators=(',', ': '))

	# write it to file
	jsonout = open("quickstore.json", "w+")
	jsonout.write(jsonstring)
	jsonout.close()

	# print done
	#cgiprint("Updated quickstore.json !!!<br>")

except Exception, err:
	exc_type, exc_value, exc_tb = sys.exc_info()
	lines = pformat(traceback.format_exception(exc_type, exc_value, exc_tb))
	
	print "<font color='red'><h2>500 Error</h2>"
	print "".join(ast.literal_eval(lines)).replace("\n", "<br>\n").replace("\\n", "<br>\n")
	