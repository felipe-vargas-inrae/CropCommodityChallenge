## Step 1

Add commodity Id and create Commodity Database

## Step 2
Set data types for dates and numbers

Remove groups commodity-APMC which don't have at least one year of information

Remove outliers based on formula 

	THRESHOLD=2
	smaller=mean-THRESHOLD*std
	bigger=mean+THRESHOLD*std

	#print(len(group))
	group=group.query('@smaller <= min_price <= @bigger')