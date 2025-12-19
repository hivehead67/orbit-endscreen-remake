import NeditGD
import random 
from collections import defaultdict
import math

step_quality = 4 #dont use multiples of 3 or other numbers that result in repeating decimals consistantly
anti_kick_scale = 20

offset = (300,300)

def rotate_point_origin(x, y, angle_rad):
    new_x = x * math.cos(angle_rad) - y * math.sin(angle_rad)
    new_y = x * math.sin(angle_rad) + y * math.cos(angle_rad)
    return new_x, new_y


def run(pos_list,drop_time,FPS):

    objects = [36,84,141,1022,1330,1333,1704,1751,3004]

    editor = NeditGD.Editor.load_live_editor()
    made_groups = []
    NeditGD.Editor.remove_scripted_objects(editor)
    keyframes = []
    spawns = []
    objs = []


    speed = 10.3761348898
    # Make all the necessary changes (add/delete objects)
    groups = defaultdict(list)
    for item in pos_list:
        key = item[0] # Get the first value
        groups[key].append(item)

    # Convert dictionary values to a list of lists if needed
    split_pos = list(groups.values())

    for i in range(len(split_pos)):
        split_pos[i] = split_pos[i][::step_quality]
        
    editor.add_object(
        NeditGD.Object(id=2016,x=285,y=-68,groups=[9998]))

    editor.add_object(
        NeditGD.Object(id=1914,x=-135,y=70,target_pos=9998,follow_group=9998))
    editor.add_object(
        NeditGD.Object(id=3613,x=-135,y=100,target_pos=9998,target=9995,x_ref=2))
    editor.add_object(
        NeditGD.Object(id=3022,x=15,y=165,target=9996))
    editor.add_object(
        NeditGD.Object(id=1007,x=0,y=-30,target=9994))

    for n in split_pos:
        for i in range(len(n)):
            info = n[i]
            if info[6] == False:
                editor.add_object(
                    NeditGD.Object(id=3032, x=info[1]*anti_kick_scale-300, y=info[2]*-1*anti_kick_scale, groups=[info[0],9997], duration=1/(FPS/step_quality), rotation=math.degrees(info[4]),frame_index=i-1,anim_id=info[0]))
                keyframes.append(info[0])
                if not info[0] in made_groups:
                    orb = random.choice(objects)
                    made_groups.append(info[0])
                    if orb == 1022 or orb == 1330:
                        editor.add_object(
                            NeditGD.Object(id=orb, x=info[1]-300, y=info[2]*-1-210, groups=[len(made_groups),9997,9995], scale=info[5]/15, editor_layer_1=2))
                    else:
                        editor.add_object(
                            NeditGD.Object(id=orb, x=info[1]-300, y=info[2]*-1-210, groups=[len(made_groups),9997,9995], scale=info[5]/15))
                objs.append(len(made_groups))
                spawns.append(info[3])
            elif i > 0:
                editor.add_object(
                            NeditGD.Object(id=2015, x=((info[3]+(i*step_quality)) / FPS) * 311.6, y=-60, rotate_degrees=math.degrees(info[4])*-1,duration=step_quality/FPS))
                editor.add_object(
                            NeditGD.Object(id=1346, x=((info[3]+(i*step_quality)) / FPS) * 311.6, y=-120, rotate_degrees=math.degrees(n[i-1][4]-info[4])*-1, target=9998,target_pos=9996,duration=step_quality/FPS))
                

                rotated = rotate_point_origin((info[1]-n[i-1][1]),(info[2]-n[i-1][2]),info[4])
                editor.add_object(
                            NeditGD.Object(id=901, x=((info[3]+(i*step_quality)) / FPS) * 311.6, y=-90,move_x=rotated[0]*-1,move_y=rotated[1],small_step=True,target=9998,duration=step_quality/FPS))

            else:
                rotated = rotate_point_origin((info[1]),(info[2]),info[4])
                editor.add_object(
                        NeditGD.Object(id=1764,x=round((600/40)*15,2)+30,y=round((400/40)*15,2)+30+75+7.5,groups=[9996,9994],hide=True))
                editor.add_object(
                        NeditGD.Object(id=1,x=round((600/40)*15,2)+30,y=round((400/40)*15,2)+75+7.5,hide=True,groups=[9994]))
                editor.add_object(
                        NeditGD.Object(id=1613, x=((info[3]) / FPS) * 311.6, y=30))
                #editor.add_object(
                #        NeditGD.Object(id=901, x=((info[3]) / FPS) * 311.6, y=-90,move_x=rotated[0]*-1,move_y=rotated[1],small_step=True,target=9998,duration=step_quality/FPS))

                

    made_setups = []

    for n in range(len(spawns)):
        if not spawns[n] in made_setups:
            editor.add_object(
                NeditGD.Object(
                    id=3033,
                    x=(spawns[n] / FPS) * 311.6,
                    y=0,
                    animation_id=keyframes[n],
                    target=objs[n],
                    time_mod_2=1,
                    position_x_mod=1/anti_kick_scale,
                    position_y_mod=1/anti_kick_scale,
                    rotation_mod=1,
                    scale_x_mod=1,
                    scale_y_mod=1,
                )
            )
            made_setups.append(spawns[n])
    
    editor.add_object(
        NeditGD.Object(id=901, x=0, y=0,move_x=offset[0],move_y=offset[1],small_step=True,target=9999))
    editor.add_object(
        NeditGD.Object(id=1612, x=0, y=-30))
            

    editor.save_changes()