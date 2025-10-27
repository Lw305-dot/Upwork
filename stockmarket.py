import requests
import pandas as pd

# Define API endpoint and headers
url = "https://public-api.wordpress.com/wpcom/v2/work-with-us"
HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "X-future": "automattician"}
# Make the request
response = requests.get(url, headers=HEADERS)

# Check the status
print("Status Code:", response.status_code)

# Proceed if successful
if response.status_code == 200:
    # Parse JSON response
    data = response.json()
    
    # Extract "routes"
    routes = data.get("routes", {})
    
    # Convert to DataFrame
    routes_df = pd.DataFrame.from_dict(routes, orient='index')
    
    # Preview the DataFrame
    print("DataFrame preview:")
    print(routes_df.head())

    # Save to Excel
    output_file = "wordpress_api_routes3.xlsx"
    routes_df.to_excel(output_file, index=True)
    print(f"\n✅ Excel file saved as: {output_file}")

else:
    print("❌ Failed to fetch data from the API.")

