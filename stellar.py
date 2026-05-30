import turtle
import math
import random

WIDTH, HEIGHT = 1200, 800

COLOR_SPACE_VOID = "#010103"
COLOR_GLOW_CORE   = "#ffffff"
COLOR_GLOW_INNER  = "#fff1c2"
COLOR_GLOW_MID    = "#ffaa44"
COLOR_GLOW_OUTER  = "#d43d1a"
COLOR_HUD_BG     = "#03060d"
COLOR_HUD_EDGE   = "#00f0ff"
COLOR_HUD_MUTED  = "#3b597a"
COLOR_HUD_TEXT   = "#ffffff"

CELESTIAL_REGISTRY = {
    "Mercury": {"radius": 3.5, "distance": 130, "velocity": 0.045, "color": "#9ca3af", "data": "Dist: 57.9M km | Period: 88d | Temp: 167°C"},
    "Venus":   {"radius": 7.0, "distance": 180, "velocity": 0.032, "color": "#fbbf24", "data": "Dist: 108.2M km | Period: 224.7d | Temp: 464°C"},
    "Earth":   {"radius": 8.0, "distance": 240, "velocity": 0.024, "color": "#3b82f6", "data": "Dist: 149.6M km | Period: 365.2d | Temp: 15°C"},
    "Mars":    {"radius": 5.5, "distance": 300, "velocity": 0.018, "color": "#ef4444", "data": "Dist: 227.9M km | Period: 687d | Temp: -65°C"},
    "Jupiter": {"radius": 19.0, "distance": 400, "velocity": 0.010, "color": "#f59e0b", "data": "Dist: 778.5M km | Period: 12y | Temp: -110°C"},
    "Saturn":  {"radius": 15.0, "distance": 510, "velocity": 0.007, "color": "#eab308", "data": "Dist: 1.4B km | Period: 29y | Rings: True"},
    "Uranus":  {"radius": 11.0, "distance": 610, "velocity": 0.005, "color": "#06b6d4", "data": "Dist: 2.8B km | Period: 84y | Temp: -195°C"},
    "Neptune": {"radius": 10.5, "distance": 700, "velocity": 0.004, "color": "#4f46e5", "data": "Dist: 4.5B km | Period: 164.8y | Temp: -200°C"}
}

engine_state = {
    "active_target": "Global View",
    "status_feed": "Use W A S D / Arrows to Orbit Viewport,  CTRL +/- to Zoom.",
    "render_orbits": True,
    "stellar_particles": [],
    "orbital_positions": {body: random.uniform(0, 2 * math.pi) for body in CELESTIAL_REGISTRY},
    "camera_pitch": 1.1,  
    "camera_yaw": 0.5,    
    "camera_zoom": 0.8,   
    "camera_distance": 1200,
    "projected_cache": {} 
}

screen = turtle.Screen()
screen.setup(WIDTH, HEIGHT)
screen.bgcolor(COLOR_SPACE_VOID)
screen.title("STELLAR WIND = Solar System")
screen.tracer(0, 0)

layer_deep_space = turtle.Turtle()
layer_deep_space.hideturtle()

layer_dynamic_render = turtle.Turtle()
layer_dynamic_render.hideturtle()

layer_hud_interface = turtle.Turtle()
layer_hud_interface.hideturtle()


def project_3d_to_2d(x, y, z):
    """Transforms native 3D spatial points into high-accuracy 2D isometric perspectives."""
    cos_y = math.cos(engine_state["camera_yaw"])
    sin_y = math.sin(engine_state["camera_yaw"])
    x1 = x * cos_y - z * sin_y
    z1 = x * sin_y + z * cos_y
    
    cos_p = math.cos(engine_state["camera_pitch"])
    sin_p = math.sin(engine_state["camera_pitch"])
    y2 = y * cos_p - z1 * sin_p
    z2 = y * sin_p + z1 * cos_p

    depth_factor = engine_state["camera_distance"] / (engine_state["camera_distance"] + z2)
    screen_x = x1 * engine_state["camera_zoom"] * depth_factor * 1.3
    screen_y = y2 * engine_state["camera_zoom"] * depth_factor * 1.3
    
    return screen_x, screen_y, z2

def generate_deep_space_matrix():
    """Generates a high-density, multi-weighted 3D coordinate stellar field."""
    engine_state["stellar_particles"] = []
    for _ in range(450):
        r = random.randint(300, 1500)
        theta = random.uniform(0, 2 * math.pi)
        phi = random.uniform(-math.pi/3, math.pi/3)
        x = r * math.cos(theta) * math.cos(phi)
        y = r * math.sin(phi)
        z = r * math.sin(theta) * math.cos(phi)
        weight = random.choice([1, 1.5, 2])
        luminance = random.choice(["#141933", "#29153b", "#3b1a40", "#ffffff", "#446699"])
        engine_state["stellar_particles"].append((x, y, z, weight, luminance))

def render_volumetric_core_3d(t, x_base, y_base, base_radius, scale_mod):
    """Simulates an anti-aliased WebGL volumetric light flare via additive radial drawing."""
    r = base_radius * scale_mod
    if r < 2: r = 2

    t.penup()
    t.goto(x_base, y_base - (r * 2.8))
    t.color(COLOR_GLOW_OUTER)
    t.begin_fill()
    t.circle(r * 2.8)
    t.end_fill()
    
    t.goto(x_base, y_base - (r * 1.8))
    t.color(COLOR_GLOW_MID)
    t.begin_fill()
    t.circle(r * 1.8)
    t.end_fill()
    
    t.goto(x_base, y_base - (r * 1.3))
    t.color(COLOR_GLOW_INNER)
    t.begin_fill()
    t.circle(r * 1.3)
    t.end_fill()
    
    t.goto(x_base, y_base - r)
    t.color(COLOR_GLOW_CORE)
    t.begin_fill()
    t.circle(r)
    t.end_fill()

def execute_hud_draw():
    """Renders a non-overlapping, high-tech telemetry dashboard layout."""
    layer_hud_interface.clear()
    panel_left = -WIDTH//2 + 30
    panel_top = HEIGHT//2 - 30
    panel_width = 460
    panel_height = 175
    
    layer_hud_interface.penup()
    layer_hud_interface.goto(panel_left, panel_top)
    layer_hud_interface.color(COLOR_HUD_EDGE, COLOR_HUD_BG)
    layer_hud_interface.pensize(1)
    layer_hud_interface.pendown()
    
    layer_hud_interface.begin_fill()
    for _ in range(2):
        layer_hud_interface.forward(panel_width)
        layer_hud_interface.right(90)
        layer_hud_interface.forward(panel_height)
        layer_hud_interface.right(90)
    layer_hud_interface.end_fill()
    
    layer_hud_interface.penup()
    layer_hud_interface.goto(panel_left, panel_top - 32)
    layer_hud_interface.pendown()
    layer_hud_interface.forward(panel_width)
    
    layer_hud_interface.penup()
    layer_hud_interface.color(COLOR_HUD_EDGE)
    layer_hud_interface.goto(panel_left + 20, panel_top - 24)
    layer_hud_interface.write(f" TARGET: {engine_state['active_target'].upper()}", font=("Courier New", 10, "bold"))
    
    layer_hud_interface.color(COLOR_HUD_TEXT)
    layer_hud_interface.goto(panel_left + 20, panel_top - 58)
    layer_hud_interface.write(f"Camera: Pitch={engine_state['camera_pitch']:.2f} radius | Scale={engine_state['camera_zoom']:.2f}x", font=("Consolas", 9, "normal"))
        
    layer_hud_interface.goto(panel_left + 20, panel_top - 84)
    layer_hud_interface.write(engine_state["status_feed"], font=("Consolas", 9, "normal"))
    
    layer_hud_interface.color(COLOR_HUD_MUTED)
    layer_hud_interface.goto(panel_left + 20, panel_top - 116)
    layer_hud_interface.write(">> SPACE VIEWPORT: [W/S/A/D or Arrows to Move Camera Axis]", font=("Courier New", 7, "bold"))
    layer_hud_interface.goto(panel_left + 20, panel_top - 134)
    layer_hud_interface.write(">> RANGE SCALING:  [Press Plus '+' to Zoom In | Minus '-' to Zoom Out]", font=("Courier New", 7, "bold"))
    layer_hud_interface.goto(panel_left + 20, panel_top - 152)
    layer_hud_interface.write(">> DATA TRACKING:  [Click Body to Intercept Map Vectors | 'O' for Orbit Grid]", font=("Courier New", 7, "bold"))

def process_frame_tick():
    """Calculates high-accuracy 3D orbital paths and schedules isolated components."""
    layer_dynamic_render.clear()
    engine_state["projected_cache"].clear()
    
    render_queue = []
    
    for sx, sy, sz, sw, scol in engine_state["stellar_particles"]:
        px, py, pz = project_3d_to_2d(sx, sy, sz)
        if -WIDTH//2 < px < WIDTH//2 and -HEIGHT//2 < py < HEIGHT//2:
            render_queue.append({
                "type": "star", "depth": pz, "x": px, "y": py, "weight": sw, "color": scol
            })

    sun_x, sun_y, sun_z = project_3d_to_2d(0, 0, 0)
    sun_scale = engine_state["camera_distance"] / (engine_state["camera_distance"] + sun_z)
    render_queue.append({
        "type": "sun", "depth": sun_z, "x": sun_x, "y": sun_y, "scale": sun_scale
    })

    for name, data in CELESTIAL_REGISTRY.items():
        engine_state["orbital_positions"][name] += data["velocity"]
        curr_angle = engine_state["orbital_positions"][name]
        
        bx = data["distance"] * math.cos(curr_angle)
        bz = data["distance"] * math.sin(curr_angle)
        by = 0 
        
        px, py, pz = project_3d_to_2d(bx, by, bz)
        p_scale = engine_state["camera_distance"] / (engine_state["camera_distance"] + pz)

        engine_state["projected_cache"][name] = (px, py, p_scale)
        
        render_queue.append({
            "type": "planet", "name": name, "depth": pz, "x": px, "y": py, 
            "radius": data["radius"], "color": data["color"], "scale": p_scale,
            "has_rings": data.get("has_rings", False)
        })

        if engine_state["render_orbits"]:
            orbit_steps = 72
            for i in range(orbit_steps):
                a1 = (i / orbit_steps) * 2 * math.pi
                ox = data["distance"] * math.cos(a1)
                oz = data["distance"] * math.sin(a1)
                opx, opy, opz = project_3d_to_2d(ox, 0, oz)
                
                render_queue.append({
                    "type": "orbit_dot", "depth": opz, "x": opx, "y": opy, 
                    "color": COLOR_HUD_EDGE if engine_state["active_target"] == name else "#0c152b",
                    "weight": 1.5 if engine_state["active_target"] == name else 1
                })

    render_queue.sort(key=lambda item: item["depth"], reverse=True)
    
    for obj in render_queue:
        if obj["type"] == "star":
            layer_dynamic_render.penup()
            layer_dynamic_render.goto(obj["x"], obj["y"])
            layer_dynamic_render.dot(obj["weight"], obj["color"])
            
        elif obj["type"] == "sun":
            render_volumetric_core_3d(layer_dynamic_render, obj["x"], obj["y"], 24, obj["scale"])
            
        elif obj["type"] == "orbit_dot":
            layer_dynamic_render.penup()
            layer_dynamic_render.goto(obj["x"], obj["y"])
            layer_dynamic_render.dot(obj["weight"], obj["color"])
            
        elif obj["type"] == "planet":
            r_projected = obj["radius"] * obj["scale"] * engine_state["camera_zoom"]
            if r_projected < 1.5: r_projected = 1.5
            
            layer_dynamic_render.penup()
            layer_dynamic_render.goto(obj["x"], obj["y"] - r_projected)
            layer_dynamic_render.setheading(0)
            layer_dynamic_render.color(obj["color"])
            layer_dynamic_render.begin_fill()
            layer_dynamic_render.circle(r_projected)
            layer_dynamic_render.end_fill()
            
            if obj["has_rings"]:
                layer_dynamic_render.penup()
                layer_dynamic_render.goto(obj["x"] - r_projected - (8 * obj["scale"]), obj["y"])
                layer_dynamic_render.color("#8f7647")
                layer_dynamic_render.pensize(int(2.5 * obj["scale"]) if int(2.5 * obj["scale"]) > 1 else 1)
                layer_dynamic_render.pendown()
                layer_dynamic_render.goto(obj["x"] + r_projected + (8 * obj["scale"]), obj["y"])
                layer_dynamic_render.pensize(1)
                
            layer_dynamic_render.penup()
            layer_dynamic_render.goto(obj["x"], obj["y"] + r_projected + 5)
            font_size = int(8 * obj["scale"] * engine_state["camera_zoom"])
            if font_size < 7: font_size = 7
            if font_size > 11: font_size = 11
            
            if engine_state["active_target"] == obj["name"]:
                layer_dynamic_render.color(COLOR_HUD_EDGE)
                layer_dynamic_render.write(f"▼ {obj['name']}", align="center", font=("Consolas", font_size, "bold"))
            else:
                layer_dynamic_render.color("#a1a1aa")
                layer_dynamic_render.write(obj["name"], align="center", font=("Consolas", font_size, "normal"))

    screen.update()

def process_canvas_click(x, y):
    """Processes real-time linear distance matrices to find target intercepts."""
    for name, coords in engine_state["projected_cache"].items():
        px, py, p_scale = coords
        linear_distance = math.sqrt((x - px)**2 + (y - py)**2)
        
        click_boundary = 25 * p_scale
        if click_boundary < 15: click_boundary = 15
        
        if linear_distance < click_boundary:
            engine_state["active_target"] = name
            engine_state["status_feed"] = CELESTIAL_REGISTRY[name]["data"]
            execute_hud_draw()
            return
            
    engine_state["active_target"] = "Global View"
    engine_state["status_feed"] = "Tracking lost. System returned to global galaxy."
    execute_hud_draw()

def cam_pitch_up():
    engine_state["camera_pitch"] = min(engine_state["camera_pitch"] + 0.08, math.pi/2 - 0.01)
    execute_hud_draw()

def cam_pitch_down():
    engine_state["camera_pitch"] = max(engine_state["camera_pitch"] - 0.08, 0.05)
    execute_hud_draw()

def cam_yaw_left():
    engine_state["camera_yaw"] += 0.08
    execute_hud_draw()

def cam_yaw_right():
    engine_state["camera_yaw"] -= 0.08
    execute_hud_draw()

def cam_zoom_in():
    engine_state["camera_zoom"] = min(engine_state["camera_zoom"] + 0.05, 2.5)
    execute_hud_draw()

def cam_zoom_out():
    engine_state["camera_zoom"] = max(engine_state["camera_zoom"] - 0.05, 0.2)
    execute_hud_draw()

def process_orbit_toggle():
    engine_state["render_orbits"] = not engine_state["render_orbits"]
    execute_hud_draw()
    
screen.onclick(process_canvas_click)
screen.onkey(cam_pitch_up, "w")
screen.onkey(cam_pitch_up, "W")
screen.onkey(cam_pitch_up, "Up")
screen.onkey(cam_pitch_down, "s")
screen.onkey(cam_pitch_down, "S")
screen.onkey(cam_pitch_down, "Down")
screen.onkey(cam_yaw_left, "a")
screen.onkey(cam_yaw_left, "A")
screen.onkey(cam_yaw_left, "Left")
screen.onkey(cam_yaw_right, "d")
screen.onkey(cam_yaw_right, "D")
screen.onkey(cam_yaw_right, "Right")
screen.onkey(cam_zoom_in, "+")
screen.onkey(cam_zoom_in, "=")
screen.onkey(cam_zoom_out, "-")
screen.onkey(process_orbit_toggle, "o")
screen.onkey(process_orbit_toggle, "O")

screen.listen()

generate_deep_space_matrix()
execute_hud_draw()

def runtime_loop():
    process_frame_tick()
    screen.ontimer(runtime_loop, 16)

runtime_loop()
screen.mainloop()