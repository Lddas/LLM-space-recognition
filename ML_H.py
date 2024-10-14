from flask import Flask, render_template, jsonify
from openai import OpenAI
import logging
import webbrowser

# Initialize the client
client = OpenAI()

app = Flask(__name__)

goal_room = "F38"
ML_goal = "ML_11"
direction_goal = "right"
current_position = "ML_1"
path = ["ML_1"]
path_urls = []
mislead = 0
misleading = 0

possible_next = {
    "ML_1": {"left": "ML_7"},
    "ML_2": {"left": "ML_3"},
    "ML_3": {"right": "ML_4"},
    "ML_4": {"forward": "ML_5", "right": "ML_6"},
    "ML_5": {},
    "ML_6": {},
    "ML_7": {"forward": "ML_8"},
    "ML_8": {"forward": "ML_9"},
    "ML_9": {"forward": "ML_10"},
    "ML_10": {"forward": "ML_11"},
    "ML_11": {},
    "ML_12": {"forward": "ML_13"},
    "ML_13": {},
    "ML_14": {"forward": "ML_15"},
    "ML_15": {"forward": "ML_16"},
    "ML_16": {"forward": "ML_17"},
    "ML_17": {},
    "ML_20": {"forward": "ML_21", "left": "ML_25"},
    "ML_21": {},
    "ML_25": {"forward": "ML_26", "left": "ML_14"},
    "ML_26": {}
}

conversation_history = [
    {"role": "system", "content": f"""We will be navigating in a building, step by step. It is your mission to understand how the room numerotation works. 
                                    We are in Switzerland, so the floor representation works with letters. We enter the building in floor D, E being upstairs, C downstairs.
                                    You can only use staircases, not elevators.
                                    The goal is to find the room {goal_room}. At each step, I will be giving you 3 images of my surroundings, and you will tell me in which 
                                    direction you want to continue. If you want to go backward, I will just give you the precedent 3 pictures. 
                                    We will continue until you can detect the goal room number somewhere on a picture. Do you understand everything ?"""},
]

def ask_gpt_direction(image_urls):
    global mislead, misleading
    image_prompt = [
        {"type": "text", 
        "text": f"""I want to find room {goal_room}. Here are 3 images of my surroundings. 
                        The first one is on my left, the second is in front of me, and the third is on my right. 
                        You should be able to see the room numbers if there are any. Where do you want to go next in order to find the goal? 
                        Please give me 2 sentences to describe your reasoning in order to find the goal room.
                        VERY IMPORTANT: The first image is on my left, the second image is in front of me, and the third image is on my right. The last word of your answer must be one of these 4 words to say where you want to go next: forward, right, left, backward."""
        },
        {"type": "image_url", "image_url": {"url": f"{image_urls[0]}"}},  # Left image
        {"type": "image_url", "image_url": {"url": f"{image_urls[1]}"}},  # Front image
        {"type": "image_url", "image_url": {"url": f"{image_urls[2]}"}},  # Right image
    ]

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=conversation_history + [
            {"role": "user", "content": image_prompt}
        ],
        max_tokens=100
    )

    conversation_history.append({"role": "assistant", "content": response.choices[0].message.content})
    print(f"Model's choice: {response.choices[0].message.content}")

    user_message = f"""For the recall, the left image (1st one) is on my left, the forward image (2nd one) is in front of me, and the right image (3rd one) is on my right side. 
                        If you want to go toward the first image, go LEFT. If you want to go toward the second image, go FORWARD. If you want to go toward the third image, go RIGHT."""
    conversation_history.append({"role": "user", "content": user_message})

    if mislead:
        user_message = f"""{user_message} As you saw, {misleading} is not a good choice. Please choose something else. """
        mislead = False
        print("user_message errooooooor", user_message)

    direction_response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=conversation_history + [
            {"role": "user", "content": [
                {"type": "text", "text": f"""{user_message}
                                            Now, giving what we just said together, give me the next direction you want to go. Don't forget that you can go backward if no option looks satisfying.
                                            VERY IMPORTANT: Answer only by one of these 4 words to say where you want to go next: forward, right, left, backward."""}
            ]}
        ],
        max_tokens=50
    )


    return direction_response.choices[0].message.content

def path_pic(direction, urls):
    if direction == "left":
        path_urls.append(urls[0])
    elif direction == "forward":
        path_urls.append(urls[1])
    elif direction == "right":
        path_urls.append(urls[2])


@app.route('/')
def index():
    global current_position
    nb = int(current_position.split('_')[-1])
    image_urls = [
        f"https://raw.githubusercontent.com/alexxelaalexxela/LLM-space-recognition-/LEE_visit/{nb}_LEFT.jpg",
        f"https://raw.githubusercontent.com/alexxelaalexxela/LLM-space-recognition-/LEE_visit/{nb}_FORWARD.jpg",
        f"https://raw.githubusercontent.com/alexxelaalexxela/LLM-space-recognition-/LEE_visit/{nb}_RIGHT.jpg"
    ]
    return render_template('index.html', image_urls=image_urls, current_position=current_position, path=path)

@app.route('/get_next_direction', methods=['GET'])
def get_next_direction():
    global current_position, goal_room, ML_goal, direction_goal, path, path_urls, mislead, misleading

    nb = int(current_position.split('_')[-1])
    image_urls = [
        f"https://raw.githubusercontent.com/alexxelaalexxela/LLM-space-recognition-/LEE_visit/{nb}_LEFT.jpg",
        f"https://raw.githubusercontent.com/alexxelaalexxela/LLM-space-recognition-/LEE_visit/{nb}_FORWARD.jpg",
        f"https://raw.githubusercontent.com/alexxelaalexxela/LLM-space-recognition-/LEE_visit/{nb}_RIGHT.jpg"
    ]

    direction = ask_gpt_direction(image_urls)
    print("direction", direction)
    if not direction:
        return jsonify({'error': 'Failed to determine direction'}), 500

    if direction in possible_next[current_position]:
        print("parfait", direction)
        current_position = possible_next[current_position][direction]
        path.append(current_position)
        path_pic(direction, image_urls)
    elif direction == "backward":
        path.pop()
        current_position = path[-1]
        path_urls.pop()
    elif direction not in possible_next[current_position] and direction != direction_goal:
        mislead = True
        misleading = direction
        print("mislead")
        return jsonify({'error': f'Unexpected direction: {direction}'}), 400
    
    '''if current_position == ML_goal and direction == direction_goal:
        success_message = f"You have reached room {goal_room}, the goal. Well done!"
        print(success_message)
        path_pic(direction, image_urls)
        for pic in path_urls:
            webbrowser.open(pic)'''
    

    new_nb = int(current_position.split('_')[-1])
    new_image_urls = [
        f"https://raw.githubusercontent.com/alexxelaalexxela/LLM-space-recognition-/LEE_visit/{new_nb}_LEFT.jpg",
        f"https://raw.githubusercontent.com/alexxelaalexxela/LLM-space-recognition-/LEE_visit/{new_nb}_FORWARD.jpg",
        f"https://raw.githubusercontent.com/alexxelaalexxela/LLM-space-recognition-/LEE_visit/{new_nb}_RIGHT.jpg"
    ]

    if current_position == ML_goal and direction == direction_goal:
        success_message = f"You have reached room {goal_room}, the goal. Well done!"
        logging.info(success_message)
        path_pic(direction, image_urls)

        return jsonify({
            'image_urls': new_image_urls,
            'current_position': current_position,
            'path': path,
            'goal_reached': True,
            'chosen_direction': direction,
            'path_urls': path_urls  # Include path_urls in the response
        })
    else:
        return jsonify({
            'image_urls': new_image_urls,
            'current_position': current_position,
            'path': path,
            'goal_reached': False,
            'chosen_direction': direction
        })

if __name__ == '__main__':
    app.run(debug=True)
