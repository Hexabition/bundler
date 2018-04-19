import config
import os
import shutil
import json
from git import Repo
from tqdm import tqdm

def gif_path(name):
    return "{0}/{1}.gif".format(config.output_gif_dir, name.replace(' ', '_'))

def showreel_path(name):
    return "{0}/{1}.mp4".format(config.output_showreel_dir, name.replace(' ', '_'))

def animation_path(id):
    return "{0}/{1}.mp4".format(config.output_animation_dir, str(id))

def name_from_file(file):
    name = file.replace('.mp4', '')
    return name.replace('_', ' ')

def config_for_name(name):
    return {
        "creator": name,
        "backgroundImagePath": gif_path(name),
        "path": showreel_path(name)
    }

def people_config(dir):
    people = []
    dir_path = os.path.join(config.showreel_dir, dir)
    for file in tqdm(os.listdir(dir_path)):
        file_path = os.path.join(dir_path, file)
        name = name_from_file(file)
        people.append(config_for_name(name))
    return people

def tablet_config(dir):
    people = people_config(dir)
    id = int(dir)

    mqtt_id = 100 + id
    mqtt_config = config.mqtt
    mqtt_config['id'] = mqtt_id
    return {
        'id': id,
        'animation': False,
        'mqtt': mqtt_config,
        'people': people
    }

def animation_config(file):
    id = int(file.replace('.mp4', ''))
    mqtt_id = 200 + id
    mqtt_config = config.mqtt
    mqtt_config['id'] = mqtt_id

    return {
        'id': id,
        'animation': animation_path(id),
        'mqtt': mqtt_config,
        'people': False
    }

def dump_config(tablet_config, dir):
    with open(os.path.join(dir, config.config_path), 'w') as outfile:
        json.dump(tablet_config, outfile)    

def bundle_with_config(tablet_config):
    if tablet_config['animation']:
        output_dir = os.path.join(config.output_dir, "Animation-"+str(tablet_config['id']))

        Repo.clone_from(config.git_url, output_dir)

        video_dir = os.path.join(output_dir, config.output_animation_dir)
        anim_file = os.path.join(config.animation_dir, str(tablet_config['id']) + '.mp4')
        os.makedirs(video_dir, exist_ok=True)
        shutil.copy2(anim_file, video_dir)
        dump_config(tablet_config, output_dir)

    elif tablet_config['people']:
        output_dir = os.path.join(config.output_dir, "Player-"+str(tablet_config['id']))
        Repo.clone_from(config.git_url, output_dir)

        video_dir = os.path.join(output_dir, config.output_showreel_dir)
        gif_dir = os.path.join(output_dir, config.output_gif_dir)

        os.makedirs(video_dir, exist_ok=True)
        os.makedirs(gif_dir, exist_ok=True)
        input_video_dir = os.path.join(config.showreel_dir, str(tablet_config['id']))
        for file in tqdm(os.listdir(input_video_dir)):
            file_path = os.path.join(input_video_dir, file)
            shutil.copy2(file_path, video_dir)
        dump_config(tablet_config, output_dir)

def bundle_people():
    for dir in tqdm(os.listdir(config.showreel_dir)):
        tconfig = tablet_config(dir)
        bundle_with_config(tconfig)

def bundle_animations():
    for file in tqdm(os.listdir(config.animation_dir)):
        aconfig = animation_config(file)
        bundle_with_config(aconfig)

if __name__ == "__main__":
  bundle_people()
  bundle_animations()
    
