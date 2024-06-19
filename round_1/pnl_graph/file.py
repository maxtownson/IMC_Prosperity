import csv

# Function to separate data for AMETHYSTS and STARFRUIT and write to CSV files
def createStarandAmyCSV(input_csv, amethysts_csv, starfruit_csv):
    amethysts_data = []
    starfruit_data = []

    with open(input_csv, 'r') as file:
        reader = csv.DictReader(file, delimiter=';')
        for row in reader:
            if row['product'] == 'AMETHYSTS':
                amethysts_data.append(row)
            elif row['product'] == 'STARFRUIT':
                starfruit_data.append(row)

    # Write AMETHYSTS data to CSV
    with open(amethysts_csv, 'w', newline='') as amethysts_file:
        writer = csv.DictWriter(amethysts_file, fieldnames=reader.fieldnames, delimiter=';')
        writer.writeheader()
        writer.writerows(amethysts_data)

    # Write STARFRUIT data to CSV
    with open(starfruit_csv, 'w', newline='') as starfruit_file:
        writer = csv.DictWriter(starfruit_file, fieldnames=reader.fieldnames, delimiter=';')
        writer.writeheader()
        writer.writerows(starfruit_data)

# Example usage
input_csv_path = 'historical_data.csv'           
amethysts_csv_path = 'amethysts_data.csv'   
starfruit_csv_path = 'starfruit_data.csv'   

createStarandAmyCSV(input_csv_path, amethysts_csv_path, starfruit_csv_path)