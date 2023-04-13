
def change_file_users(file_name):
    # Read the JSON file as plain text

    
    with open(file_name, 'r') as file:
        json_text = file.read()

    user = ["f0898_29", "f0858_32", "f0863_41", "f0815_12", "f0895_48", "f0813_02", "f0880_16", "f0833_32", "f0817_40", "f0871_23"]
    json_text = json_text.replace(user[0], "0").replace(user[1], "1").replace(user[2], "2").replace(user[3], "3").replace(user[4], "4").replace(user[5], "5").replace(user[6], "6").replace(user[7], "7").replace(user[8], "8").replace(user[9], "9")

    # Write the modified JSON text back to the file
    with open(file_name, 'w') as file:
        file.write(json_text)

# Load the modified JSON data
# json_data = json.loads(json_text)

file_name = 'all_data_8_niid_1_keep_3_'
change_file_users('./train/'+file_name+'train_9.json')
change_file_users('./test/'+file_name+'test_9.json')