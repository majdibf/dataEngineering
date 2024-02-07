import pandas as pd
import numpy as np

bank_marketing_df = pd.read_csv('bank_marketing.csv')
bank_marketing_df['year'] = 2022

# client
client_cols = ['client_id', 'age', 'job', 'marital', 'education', 'credit_default', 'mortgage']
client = bank_marketing_df[client_cols]
# Change "." to "_"
client['job'] = client['job'].str.replace('.', '_')
# Change "." to "_" and "unknown" to np.NaN
client['education'] = client['education'].str.replace('.', '_')
client['education'] = client['education'].replace('unknown', np.nan)
# Convert colone to boolean data type: yes -> True no ->False others -> NaN
client['credit_default'] = client['credit_default'].map(lambda val: True if val == 'yes' else False)  # not specified mapping will be converted to NaN
client['mortgage'] = client['mortgage'].map(lambda val: True if val == 'yes' else False)

client.to_csv('client.csv', index=False)

# campaign
campaign_cols = ['client_id', 'number_contacts', 'contact_duration', 'previous_campaign_contacts', 'previous_outcome', 'campaign_outcome', 'day', 'month', 'year']
campaign = bank_marketing_df[campaign_cols]
campaign['previous_outcome'] = campaign['previous_outcome'].map({'nonexistent': False, 'failure': False, 'success': True})
campaign['campaign_outcome'] = campaign['campaign_outcome'].map({'no': False, 'yes': True})
campaign['last_contact_date'] = campaign['year'].astype(str) + "-" + campaign['month'].astype(str) + "-" + campaign['day'].astype(str)
campaign['last_contact_date'] = pd.to_datetime(campaign['last_contact_date'])
campaign = campaign.drop(['day', 'month', 'year'], axis=1)
campaign.to_csv('campaign.csv', index=False)

# economics
economics_cols = ['client_id', 'cons_price_idx', 'euribor_three_months']
economics = bank_marketing_df[economics_cols]
economics.to_csv('economics.csv', index=False)