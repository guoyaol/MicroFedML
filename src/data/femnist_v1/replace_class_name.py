

# Read the JSON file as plain text
with open('test/all_data_11_niid_1_keep_3_test_9.json', 'r') as file:
    json_text = file.read()

# Replace the desired values
json_text = json_text.replace("f1142_44", "0").replace("f1123_09", "1").replace("f1148_23", "2").replace("f1143_43", "3").replace("f1195_27", "4").replace("f1115_26", "5").replace("f1126_06", "6").replace("f1114_07", "7").replace("f1122_02", "8").replace("f1191_18", "9")

# Write the modified JSON text back to the file
with open('test/all_data_11_niid_1_keep_3_test_9.json', 'w') as file:
    file.write(json_text)

# Load the modified JSON data
# json_data = json.loads(json_text)