# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# <pep8-80 compliant>

import math
import bpy
import mathutils
import addon_utils

from bpy.props import StringProperty, BoolProperty, FloatProperty, EnumProperty, IntProperty


#Begin Joint Tools

class HMRMPanelShip(bpy.types.Panel):
	"""Creates a Panel in the Create window"""
	bl_label = "Ships"
	bl_idname = "HMRM_TOOLS_SHIP"
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'TOOLS'
	bl_context = "objectmode"
	bl_category = "HW Joint Tools"
	
	bpy.types.Scene.ship_name = StringProperty(
		name = "Name",
		default = "Default")
	bpy.types.Scene.lod_num = IntProperty(
		name = "LOD",
		min = 0,
		max = 3,
		default = 0)
	bpy.types.Scene.flag_uv = BoolProperty(
		name = "Has Badge")
	bpy.types.Scene.flag_tags = BoolProperty(
		name = "Do Scar")
	
	def draw(self, context):
		layout = self.layout
		scn = context.scene
		
		layout.label("Ship")
		layout.prop(scn,'flag_uv')
		layout.prop(scn,'flag_tags')
		layout.prop(scn, 'ship_name')
		layout.prop(scn,'lod_num')
		
		layout.operator("hmrm.make_ship", "Convert to Ship")
		layout.operator("hmrm.make_col", "Copy to Collision")
		layout.operator("hmrm.name_fixer", "Fix Names")

class HMRMPanelTools(bpy.types.Panel):
	"""Creates a Panel in the Create window"""
	bl_label = "Hardpoints"
	bl_idname = "HMRM_TOOLS"
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'TOOLS'
	bl_context = "objectmode"
	bl_category = "HW Joint Tools"
	
	
	bpy.types.Scene.hardpoint_name = StringProperty(
		name = "Name",
		default = "Default")
	bpy.types.Scene.hardpoint_num = IntProperty(
		name = "Number",
		min = 0)
	bpy.types.Scene.weapon_mesh_name = StringProperty(
		name = "Name",
		default = "Default")
		
		
	bpy.types.Scene.utility_name = IntProperty(
		name = "Hardpoint",
		min = 0)
		
		
	bpy.types.Scene.parent_ship = StringProperty(
		name = "Ship JNT")
	
	
	def draw(self, context):
		layout = self.layout
		scn = context.scene
		
		layout.label("Weapons")
		layout.prop(scn, 'hardpoint_name')
		layout.prop(scn,'hardpoint_num')
		layout.operator("hmrm.make_weapon", "Weapon").createOptions = "Gun"
		layout.operator("hmrm.make_weapon", "Turret").createOptions = "Turret"
		
		layout.separator()
		
		layout.label("Weapon Mesh")
		layout.prop_search(scn, "parent_ship", scn, "objects")
		#layout.prop(scn, 'weapon_mesh_name')
		layout.prop(scn,'hardpoint_num')
		layout.operator("hmrm.make_weapon", "Mesh to Weapon").createOptions = "Mesh"
		
		layout.separator()
		
		layout.label("Utilities & Subsystems")
		layout.prop(scn,'utility_name')
		layout.operator("hmrm.make_hardpoint", "Repair").hardName = "RepairPoint"
		layout.operator("hmrm.make_hardpoint", "Salvage").hardName = "SalvagePoint"
		layout.operator("hmrm.make_hardpoint","Capture").hardName = "CapturePoint"
		layout.operator("hmrm.make_subsystem","Resource").subType = "Hardpoint_Resource"
		layout.operator("hmrm.make_subsystem","Production").subType = "HardpointProduction"
		layout.operator("hmrm.make_subsystem","Sensors").subType = "HardpointSensors"
		layout.operator("hmrm.make_subsystem","Target").subType = "Hardpoint_Target"
		layout.operator("hmrm.make_subsystem","Generic").subType = "HardpointGeneric"
		
		
        
        
class HMRMPanelEngines(bpy.types.Panel):
	"""Creates a Panel in the Create window"""
	bl_label = "Engines"
	bl_idname = "HMRM_TOOLS_ENGINES"
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'TOOLS'
	bl_context = "objectmode"
	bl_category = "HW Joint Tools"
	
	bpy.types.Scene.engine = IntProperty(
		name = "Engine",
		min = 1,
		default = 1
		)
	
	bpy.types.Scene.engine_small_flame = IntProperty(
		name = "Flame Div",
		min = 1,
		default = 5
		)
	
	def draw(self, context):
		layout = self.layout
		scn = context.scene

		layout.prop(scn,'engine')
		
		layout.label("Large")
		layout.operator("hmrm.make_engine_large","Convert Selection")
		layout.separator()
		
		layout.label("Small")		
		layout.prop(scn,'engine_small_flame')
		layout.operator("hmrm.make_engine_small","Add").useSelected = False
		layout.operator("hmrm.make_engine_small","Convert Selection").useSelected = True
		layout.operator("hmrm.make_subsystem","Engine Hardpoint").subType = "Hardpoint_Engine"


#Navlight Panel
class HMRMPanelNavLights(bpy.types.Panel):
	"""Creates a Panel in the Create Window"""
	bl_label = "Navlights"
	bl_idName = "HMRM_TOOLS_NAVLIGHTS"
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'TOOLS'
	bl_context = "objectmode"
	bl_category = "HW Joint Tools"
	
	bpy.types.Scene.navLightName = StringProperty(
		name = "Name",
		default = "Default")

	def draw(self, context):
		layout = self.layout
		scn = context.scene

		layout.label("Navlight Name")
		layout.prop(scn,'navLightName')
		layout.operator("hmrm.convert_navlight","Default").createOption = "default"
		layout.operator("hmrm.convert_navlight","Bay (No Flicker)").createOption = "nav_baynf"
		layout.operator("hmrm.convert_navlight","Bay").createOption = "nav_bays"
		layout.operator("hmrm.convert_navlight","Bridge").createOption = "nav_bridge"
		layout.operator("hmrm.convert_navlight","Missile").createOption = "nav_missile"
		layout.operator("hmrm.convert_navlight","Scaffold").createOption = "nav_scaffold"
		layout.operator("hmrm.convert_navlight","Thruster").createOption = "nav_thrust"

#Docking Panel
class HMRMPanelDockPaths(bpy.types.Panel):
	bl_label = "Docking Paths"
	bl_idName = "HMRM_TOOL_DOCKPATHS"
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'TOOLS'
	bl_context = "objectmode"
	bl_category = "HW Joint Tools"

	bpy.types.Scene.pathName = StringProperty(
		name = "Name",
		default = "path1")

	def draw (self, context):
		layout = self.layout
		scn = context.scene

		layout.label("Docking Path Name")
		layout.prop(scn,'pathName')
		layout.operator("hmrm.make_dock_path","Make Entry Path").createOption = "entryPath"
		layout.operator("hmrm.make_dock_path","Make Exit Path").createOption = "exitPath"

#Large Engine mesh converter
class MakeLargeEngine(bpy.types.Operator):
	bl_idname = "hmrm.make_engine_large"
	bl_label = "Make Large Engine"
	bl_options = {"UNDO"}
	
	
	
	def invoke(self, context, event):
		shipRoot = context.scene.objects["ROOT_LOD[0]"]
		cursorLoc = (shipRoot.matrix_world.inverted() * bpy.context.scene.cursor_location)
		localCoords = shipRoot.matrix_world.inverted()

		nozzleJoint = bpy.data.objects.new("JNT[EngineNozzle"+str(context.scene.engine)+"]",None)
		context.scene.objects.link(nozzleJoint)
		nozzleJoint.location = localCoords * bpy.context.selected_objects[0].location
		nozzleJoint.parent = bpy.data.objects['ROOT_LOD[0]']
		axisJoint = bpy.data.objects.new("AXIS[EngineNozzle"+str(context.scene.engine)+"]",None)
		context.scene.objects.link(axisJoint)
		axisJoint.parent = nozzleJoint

		

		engineGlowMat = bpy.data.materials.new("MATGLOW[HODOR_Glow]")

		glowEnum=1

		for ob in bpy.context.selected_objects:
			ob.name = "GLOW[EngineGlow"+str(glowEnum)+"]_LOD[0]"
			ob.data.name = ob.name+"Mesh"
			ob.data.materials.append(engineGlowMat)
			ob.parent = nozzleJoint
			ob.location = 0,0,0
			ob.rotation_euler.x = -1.57079633
			bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
			glowEnum = glowEnum+1


		return{"FINISHED"}


class MakeDockPath(bpy.types.Operator):
	bl_idname = "hmrm.make_dock_path"
	bl_label = "Make Dock Path"
	bl_options = {"UNDO"}
	createOption = bpy.props.StringProperty()
	hasHoldDock = bpy.props.BoolProperty()

	def invoke(self, context,event):
		shipRoot = context.scene.objects["ROOT_LOD[0]"]
		cursorLoc = (shipRoot.matrix_world.inverted() * bpy.context.scene.cursor_location)
		localCoords = shipRoot.matrix_world.inverted()
		
		if bpy.data.objects.find('HOLD_DOCK') != -1:
			self.hasHoldDock = True
		else:
			self.hasHoldDock = False
		

		if self.hasHoldDock == False:
			holdDock = bpy.data.objects.new("HOLD_DOCK",None)
			bpy.context.scene.objects.link(holdDock)
			holdDock.parent = bpy.data.objects['ROOT_LOD[0]']
		else:
			holdDock = bpy.data.objects['HOLD_DOCK']

		if self.createOption == "entryPath":
			pathRoot = bpy.data.objects.new("DOCK["+context.scene.pathName+"]",None)
			bpy.context.scene.objects.link(pathRoot)
			pathRoot["Fam"] = "Ship Type"
			pathRoot["Link"] = "Linked Paths"
			pathRoot["Flags"] = "None"
			pathRoot["MAD"] = "Animation Index"
			pathRoot.parent = holdDock

			for x in range(0,6):
				seg = bpy.data.objects.new("SEG["+str(x)+"]",None)
				bpy.context.scene.objects.link(seg)
				seg.parent = pathRoot
				seg.empty_draw_type = "SPHERE"
				seg["Speed"] = 50
				seg["Flags"] = "None"
				seg.location = cursorLoc

		if self.createOption == "exitPath":
			pathRoot = bpy.data.objects.new("DOCK["+context.scene.pathName+"Ex]",None)
			bpy.context.scene.objects.link(pathRoot)
			pathRoot["Fam"] = "Ship Type"
			pathRoot["Link"] = "Linked Paths"
			pathRoot["Flags"] = "Exit"
			pathRoot["MAD"] = "Animation Index"
			pathRoot.parent = holdDock

			for x in range(0,3):
				seg = bpy.data.objects.new("SEG["+str(x)+"]",None)
				bpy.context.scene.objects.link(seg)
				seg.parent = pathRoot
				seg.empty_draw_type = "SPHERE"				
				seg["Speed"] = 50
				seg["Flags"] = "None"
				seg.location = cursorLoc

		return {"FINISHED"}

			 
        
class MakeShipLOD(bpy.types.Operator):
	bl_idname = "hmrm.make_ship"
	bl_label = "Create Ship"
	bl_options = {"UNDO"}
	
	def invoke(self, context, event):
	
		if bpy.context.active_object:
			jntName_info = "ROOT_INFO"
			jntName_class = "Class[MultiMesh]_Version[512]"
			jntName_LOD = "ROOT_LOD[" + str(context.scene.lod_num) + "]"
			jntName = "JNT[" + context.scene.ship_name + "]"

			#addonsFolder = str(addon_utils.paths())[2:-2]
			#bpy.ops.wm.append(filepath="//SalMesh.blend/Object/SalvagePoint visual mesh",directory=addonsFolder+"\\HW_Toolkit\\SalMesh.Blend\\Object\\",filename="SalvagePoint visual mesh")
			
			if context.scene.flag_uv:
				jntName_uv = "UVSets[2]"
			else:
				jntName_uv = "UVSets[1]"
				
			if context.scene.lod_num == 0:
				info_jnt = bpy.data.objects.new(jntName_info, None)
				context.scene.objects.link(info_jnt)
				class_jnt = bpy.data.objects.new(jntName_class, None)
				context.scene.objects.link(class_jnt)
				uv_joint = bpy.data.objects.new(jntName_uv, None)
				context.scene.objects.link(uv_joint)
				ship_jnt = bpy.data.objects.new(jntName, None)
				context.scene.objects.link(ship_jnt)
				
				
				
			LOD_jnt = bpy.data.objects.new(jntName_LOD, None)
			context.scene.objects.link(LOD_jnt)
			LOD_jnt.rotation_euler.x = 1.57079633

			if context.scene.lod_num == 0:
				class_jnt.parent = info_jnt
				uv_joint.parent = info_jnt
				ship_jnt.parent = LOD_jnt
				bpy.context.selected_objects[0].location.xyz = (0,0,0)
				
				
			bpy.context.selected_objects[0].name = "MULT[" + context.scene.ship_name + "]_LOD[" + str(context.scene.lod_num) + "]"
			bpy.context.selected_objects[0].data.name = "MULT[" + context.scene.ship_name + "]_LOD[" + str(context.scene.lod_num) + "]"
			if context.scene.flag_tags:
				bpy.context.selected_objects[0].name = bpy.context.selected_objects[0].name+"_TAGS[DoScar]"
				bpy.context.selected_objects[0].data.name = bpy.context.selected_objects[0].name
				
			if context.scene.lod_num == 0:
				bpy.context.selected_objects[0].rotation_euler.x = -1.57079633
				bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
				bpy.context.selected_objects[0].parent = ship_jnt
			else:
				bpy.context.selected_objects[0].parent = LOD_jnt
				
		else:
			self.report({'ERROR'}, "No object found. Please select object.")
			
			
		return {"FINISHED"}
    
class MakeShipCOL(bpy.types.Operator):
	bl_idname = "hmrm.make_col"
	bl_label = "Create Collision"
	bl_options = {"UNDO"}
	
	def invoke(self, context, event):
		if bpy.context.active_object:
			colName = "ROOT_COL"
			colMesh = "COL[Root]"
			
			col_jnt = bpy.data.objects.new(colName, None)
			context.scene.objects.link(col_jnt)
			
			#col_obj = bpy.context.selected_objects[0].copy()
			#context.scene.objects.link(col_obj)
			bpy.ops.object.duplicate()
			col_obj = bpy.context.active_object
			#bpy.ops.object.select_all(action='DESELECT')
			#col_obj.select = True
			
			col_obj.name = colMesh
			col_obj.data.name = colMesh
			col_obj.parent = col_jnt			
			
			col_jnt.location = bpy.context.scene.cursor_location
			col_jnt.rotation_euler.x = 1.57079633
			col_jnt.location.y = 0
			col_jnt.location.z = 0
		else:
			self.report({'ERROR'}, "No object found. Please select object.")
			
		return {"FINISHED"}
        
class MakeWeaponHardpoint(bpy.types.Operator):
	bl_idname = "hmrm.make_weapon"
	bl_label = "Add Weapon Hardpoint"
	bl_options = {"UNDO"}
	createOptions = bpy.props.StringProperty()
	hasRoot = bpy.props.BoolProperty()
	
	def invoke(self, context, event):
	
		obs = bpy.data.objects
		
		for ob in obs:
			if "ROOT_LOD[0]" in ob.name:
				self.hasRoot = True
				
		if self.createOptions == "Mesh":
			if "JNT" not in context.scene.parent_ship:
				self.report({'ERROR'}, "No parent found. Please select your ship JNT[****]")
				return {"FINISHED"}
				
		if self.hasRoot:
			tempName = context.scene.hardpoint_name  + str(context.scene.hardpoint_num)
			
			jntName_Pos = "JNT[Weapon_" + tempName + "_Position]"
			jntName_Rest = "JNT[Weapon_" + tempName + "_Rest]"
			jntName_Dir = "JNT[Weapon_" + tempName + "_Direction]"
			jntName_Muz = "JNT[Weapon_" + tempName +"_Muzzle]"
			
			shipRoot = context.scene.objects["ROOT_LOD[0]"]
			cursorLoc = (shipRoot.matrix_world.inverted() * bpy.context.scene.cursor_location)
			localCoords = shipRoot.matrix_world.inverted()
			
			if self.createOptions == "Turret":
				jntName_Lat = "JNT[Weapon_" + tempName + "_Latitude]"
				weapon_lat = bpy.data.objects.new(jntName_Lat, None)
				context.scene.objects.link(weapon_lat)
			
			if self.createOptions == "Mesh":
				jntName_Mesh = "JNT["+ context.scene.hardpoint_name +"."+str(context.scene.hardpoint_num)+"]"
				weapon_mesh = bpy.data.objects.new(jntName_Mesh, None)
				context.scene.objects.link(weapon_mesh)
				
				jntName_Lat = "JNT[Weapon_" + tempName + "_Latitude]"
				weapon_lat = bpy.data.objects.new(jntName_Lat, None)
				context.scene.objects.link(weapon_lat)
			
			weapon_pos = bpy.data.objects.new(jntName_Pos, None)
			context.scene.objects.link(weapon_pos)
			
			weapon_dir = bpy.data.objects.new(jntName_Dir, None)
			context.scene.objects.link(weapon_dir)
			
			weapon_rest = bpy.data.objects.new(jntName_Rest, None)
			context.scene.objects.link(weapon_rest)
			
			weapon_muzzle = bpy.data.objects.new(jntName_Muz, None)
			context.scene.objects.link(weapon_muzzle)
			
			#Following standard Blender workflow, create the object at the 3D Cursor location
			#Also, since the Direction and Rest joints are in local space for Postion,
			#and HODOR expects Y-Up, offset Y for Dir and Z for rest.
			#Rotate Pos 90 degrees on X to align with Blender world space.
			
			if self.createOptions == "Mesh":
				#when converting a mesh to a turret, create the weapon pos at the selected mesh's root
				weapon_mesh.location = localCoords * bpy.context.selected_objects[0].location
				weapon_pos.location = localCoords * bpy.context.selected_objects[0].location
			else:
				weapon_pos.location = cursorLoc
			weapon_dir.location.xyz = [0,10,0]
			weapon_rest.location.xyz = [0,0,10]
			weapon_muzzle.location.xyz = [0,0,.1]
			
			if self.createOptions == "Mesh":
				bpy.context.selected_objects[0].parent = weapon_pos
				bpy.context.selected_objects[0].location = [0,0,0]
				bpy.context.selected_objects[0].rotation_euler.x = -1.57079633
				bpy.ops.object.transform_apply(location=False, rotation=True,scale=False)
			
			weapon_pos.parent = context.scene.objects["ROOT_LOD[0]"]
			weapon_dir.parent = weapon_pos
			weapon_rest.parent = weapon_pos
			
			if self.createOptions == "Mesh":
				weapon_muzzle.parent = weapon_lat
				weapon_muzzle.location.xyz = [0,0,1]
			else:
				weapon_muzzle.parent = weapon_pos
				
			if self.createOptions == "Turret":
				weapon_lat.parent = weapon_pos
				weapon_lat.location.xyz = [0,2,0]
				weapon_muzzle.parent = weapon_lat
				weapon_muzzle.location.xyz = [0,0,1]
			if self.createOptions == "Mesh":
				bpy.context.selected_objects[0].name = "MULT[" + context.scene.hardpoint_name +"." + str(context.scene.hardpoint_num) + "]_LOD[0]"
				bpy.context.selected_objects[0].data.name = "MULT[" + context.scene.hardpoint_name +"." + str(context.scene.hardpoint_num) + "]_LOD[0]"
				weapon_lat.parent = weapon_pos
				weapon_lat.location.xyz = [0,2,0]
				weapon_mesh.parent = context.scene.objects[context.scene.parent_ship]
				
				
		else:
			self.report({'ERROR'}, "No root found. Please use Convert to Ship, or manually create ROOT_LOD[0]")
			
		return {"FINISHED"}


#Subsystem Maker
class MakeSubSystem(bpy.types.Operator):
	bl_idname = "hmrm.make_subsystem"
	bl_label = "Add Subsystem"
	bl_options = {"UNDO"}
	subType = bpy.props.StringProperty()	

	
	
	def invoke(self, context, event):
		self.subType = self.subType+str(context.scene.utility_name)
		
		if bpy.data.objects.get("ROOT_LOD[0]") is not None:
			shipRoot = context.scene.objects["ROOT_LOD[0]"]
			cursorLoc = (shipRoot.matrix_world.inverted() * bpy.context.scene.cursor_location)
			localCoords = shipRoot.matrix_world.inverted()

			jntName_Pos = "JNT["+self.subType+"_Position]"
			jntName_Dir = "JNT["+self.subType+"_Direction]"
			jntName_Rest = "JNT["+self.subType+"_Rest]"

			subsys_pos = bpy.data.objects.new(jntName_Pos, None)
			context.scene.objects.link(subsys_pos)
			subsys_dir = bpy.data.objects.new(jntName_Dir,None)
			context.scene.objects.link(subsys_dir)
			subsys_rest = bpy.data.objects.new(jntName_Rest,None)
			context.scene.objects.link(subsys_rest)

			
			#if self.subType != "Hardpoint_Engine":
			#	subsys_pos.rotation_euler.x = 1.57079633
			subsys_pos.parent = bpy.data.objects.get("ROOT_LOD[0]")
			subsys_pos.location = cursorLoc
			subsys_dir.parent = subsys_pos
			subsys_dir.location.xyz = [0,10,0]
			subsys_rest.parent = subsys_pos
			subsys_rest.location.xyz = [0,0,10]

		else:
			self.report({'ERROR'}, "No root found. Please use Convert to Ship, or manually create ROOT_LOD[0]")


		return {"FINISHED"}
	
	  
class MakeHardpoint(bpy.types.Operator):
	bl_idname = "hmrm.make_hardpoint"
	bl_label = "Add Hardpoint"
	bl_options = {"UNDO"}
	hardName = bpy.props.StringProperty()
	hasRoot = bpy.props.BoolProperty()
	
	def invoke(self, context, event):
		obs = bpy.data.objects
		for ob in obs:
			if "ROOT_LOD[0]" in ob.name:
				self.hasRoot = True
		
		
		
		if self.hasRoot:
			
			shipRoot = context.scene.objects["ROOT_LOD[0]"]
			cursorLoc = (shipRoot.matrix_world.inverted() * bpy.context.scene.cursor_location)
			localCoords = shipRoot.matrix_world.inverted()

			jntName_Pos = "JNT[" + self.hardName + str(context.scene.utility_name) + "]"
			jntName_Head = "JNT[" + self.hardName + str(context.scene.utility_name) + "Heading]"
			jntName_Left = "JNT[" + self.hardName + str(context.scene.utility_name) + "Left]"
			jntName_Up = "JNT[" + self.hardName + str(context.scene.utility_name) + "Up]"
			
			
			hardp_pos = bpy.data.objects.new(jntName_Pos, None)
			context.scene.objects.link(hardp_pos)
			
			hardp_head = bpy.data.objects.new(jntName_Head, None)
			context.scene.objects.link(hardp_head)
			
			
			hardp_left = bpy.data.objects.new(jntName_Left, None)
			context.scene.objects.link(hardp_left)
			
			hardp_up = bpy.data.objects.new(jntName_Up, None)
			context.scene.objects.link(hardp_up)
			
			hardp_pos.parent = context.scene.objects["ROOT_LOD[0]"]
			hardp_head.parent = hardp_pos
			
			hardp_left.parent = hardp_pos
			hardp_up.parent = hardp_pos
			
			hardp_pos.location = cursorLoc
			#hardp_pos.rotation_euler.x = 1.57079633
			hardp_up.location.xyz = [0,10,0]
			hardp_head.location.xyz = [0,0,10]
			hardp_left.location.xyz = [10,0,0]

			#if self.hardName == "SalvagePoint":
			#	bpy.ops.wm.append(filepath="//SalMesh.blend/Object/SalvagePoint visual mesh",directory=addonsFolder+"\\HW_Toolkit\\SalMesh.Blend\\Object\\",filename="SalvagePoint visual mesh")
			#	salMesh = bpy.data.objects['SalvagePoint visual mesh']
			#	salMesh.rotation_euler.x = -1.57079633
			#	salMesh.select = True
			#	bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
			#	salMesh.parent = hardp_pos
		else:
			self.report({'ERROR'}, "No root found. Please use Convert to Ship, or manually create ROOT_LOD[0]")
			
		return {"FINISHED"}
    
    
class MakeEngineSmall(bpy.types.Operator):
    bl_idname = "hmrm.make_engine_small"
    bl_label = "Create Small Engine"
    bl_options = {"UNDO"}
    useSelected = bpy.props.BoolProperty()
    hasRoot = bpy.props.BoolProperty()
    
    def invoke(self, context, event):
        
        obs = bpy.data.objects
        for ob in obs:
            if "ROOT_LOD[0]" in ob.name:
                self.hasRoot = True
                
        if self.hasRoot:
            jntNozzle = "JNT[EngineNozzle" + str(context.scene.engine) + "]"
            jntBurn = "BURN[EngineBurn" + str(context.scene.engine) + "]"
            jntShape = "ETSH[EngineShape" + str(context.scene.engine) + "]"

            shipRoot = context.scene.objects["ROOT_LOD[0]"]
            cursorLoc = (shipRoot.matrix_world.inverted() * bpy.context.scene.cursor_location)
            localCoords = shipRoot.matrix_world.inverted()
            
            engine_nozzle = bpy.data.objects.new(jntNozzle, None)
            context.scene.objects.link(engine_nozzle)
            
            engine_burn = bpy.data.objects.new(jntBurn, None)
            context.scene.objects.link(engine_burn)
            
            if self.useSelected:
                bpy.context.selected_objects[0].name = jntShape
            else:
                verts = [(0.5,-0.5,0),(0.5,0.5,0),(-0.5,-0.5,0),(-0.5,0.5,0)]
                faces = [(2,3,1,0)]
                engine_mesh = bpy.data.meshes.new(jntShape)
                engine_shape = bpy.data.objects.new(jntShape,engine_mesh)
                context.scene.objects.link(engine_shape)
                engine_shape.parent = engine_nozzle
                engine_mesh.from_pydata(verts,[],faces)
                engine_mesh.update(calc_edges=True)
            
            engine_nozzle.parent = context.scene.objects["ROOT_LOD[0]"]
            engine_burn.parent = engine_nozzle
            
            for f in range (0, context.scene.engine_small_flame):
                flameDiv = "Flame[0]_Div[" + str(f) + "]"
                flame_div = bpy.data.objects.new(flameDiv, None)
                context.scene.objects.link(flame_div)
                
                flame_div.parent = engine_burn
                flame_div.location.z = 0-f
            
            
            #engine_nozzle.rotation_euler.x = 1.57079633
            if self.useSelected:
                engine_nozzle.location = localCoords * bpy.context.selected_objects[0].location
                bpy.context.selected_objects[0].parent = engine_nozzle
                bpy.context.selected_objects[0].location.xyz = [0,0,0]
            else:
                engine_nozzle.location = cursorLoc
        else:
            self.report({'ERROR'}, "No root found. Please use Convert to Ship, or manually create ROOT_LOD[0]")
        
        return {"FINISHED"}


class ConvertToNavlight(bpy.types.Operator):
	bl_idname = "hmrm.convert_navlight"
	bl_label = "Convert Lamp to Navlight"
	bl_options = {"UNDO"}
	createOption = bpy.props.StringProperty()
	hasRoot = bpy.props.BoolProperty()

	def invoke(self,context,event):
        
            obs = bpy.data.objects
            for ob in obs:
                if "ROOT_LOD[0]" in ob.name:
                    self.hasRoot = True
                
            if self.hasRoot:
                shipRoot = context.scene.objects["ROOT_LOD[0]"]
                cursorLoc = (shipRoot.matrix_world.inverted() * bpy.context.scene.cursor_location)
                localCoords = shipRoot.matrix_world.inverted()

                if bpy.context.active_object.type == "LAMP":
                    navLight = bpy.context.active_object

                    navLight.name = 'NAVL['+context.scene.navLightName+']'
                    navLight.data["Type"] = self.createOption
                    navLight.data["Phase"] = 0.0
                    navLight.data["Freq"] = 0.0
                    navLight.data["Flags"] = "None"

                    navLight.parent = bpy.data.objects['ROOT_LOD[0]']
                    navLight.location = localCoords * navLight.location

            else:
                self.report({'ERROR'}, "No root found. Please use Convert to Ship, or manually create ROOT_LOD[0]")
            
            return {"FINISHED"}

class FixObjectNames(bpy.types.Operator):
	bl_idname = "hmrm.name_fixer"
	bl_label = "Automatically fix duplicate object names"
	bl_options = {"UNDO"}

	def invoke(self,context,event):
		obs = bpy.data.objects

		for ob in obs:
			#Fixes Weapon Names
			if "JNT[" in ob.name and "_Position" in ob.name and "Hard" not in ob.name:
				jntName = ob.name[4:-10]				
				if "].0" in ob.name and "Slave" not in ob.name:
					jntName = jntName[:-4]
					jntNum = int(jntName[-1:])
					jntName = jntName[:-1]+str(jntNum+int(ob.name[-3:]))
				elif "].0" in ob.name and "Slave" in ob.name:
					jntName=jntName[:-4]
					if jntName[-1:] is not "e":
						jntNum=int(jntName[-1:])
						jntName=jntName[:-1]+str(jntNum+int(ob.name[-3:]))
					else:
						jntName=jntName+"1"
				ob.name = "JNT["+jntName+"_Position]"
				for x in ob.children:
					if "Latitude" in x.name:
						x.name = "JNT["+jntName+"_Latitude]"
						for y in x.children:
							if "Muzzle" in y.name:
								y.name = "JNT["+jntName+"_Muzzle]"
					elif "Rest" in x.name:
						x.name = "JNT["+jntName+"_Rest]"
					elif "Direction" in x.name:
						x.name = "JNT["+jntName+"_Direction]"
					elif "Muzzle" in x.name:
						x.name = "JNT["+jntName+"_Muzzle]"
					if "MULT[" in x.name:
						x.name = "MULT["+jntName[7:-1]+"."+jntName[-1:]+"]_LOD[0]"
						x.data.name = x.name
			#Fixes Repair, Salvage, and Capture Point Names
			if "JNT[" in ob.name and ("Repair" in ob.name or "Salvage" in ob.name or "Capture" in ob.name):
				jntName = ob.name[:-1]
				if "].0" in ob.name:
					jntName = jntName[:-4]
					jntNum = int(jntName[-1:])
					jntName = jntName[:-1]+str(jntNum+int(ob.name[-3:]))
				ob.name = jntName+"]"
				for x in ob.children:
					if "Heading" in x.name:
						x.name = jntName+"Heading]"
					elif "Left" in x.name:
						x.name = jntName+"Left]"
					elif "Up" in x.name:
						x.name = jntName+"Up]"

			#Fixes Resource, Production, Sensors, Target, and Generic hardpoints
			if "JNT[" in ob.name and "_Position" in ob.name and "Hard" in ob.name:
				jntName = ob.name[4:-10]				
				if "].0" in ob.name:
					jntName = jntName[:-4]
					jntNum = int(jntName[-1:])
					jntName = jntName[:-1]+str(jntNum+int(ob.name[-3:]))
				ob.name = "JNT["+jntName+"_Position]"
				for x in ob.children:
					if "Direction" in x.name:
						x.name = "JNT["+jntName+"_Direction]"
					elif "Rest" in x.name:
						x.name = "JNT["+jntName+"_Rest]"


						
		return {"FINISHED"}
