# Playdate App

![ERD](./PlaydateApp%20ERD%20(3).jpeg)
### Relationships
- Profiles belong to User
- User has many Profiles
- Profiles have many My Scheduled Playdates through Invites for Playdates
- My Scheduled Playdates have many Profiles through Invites for Playdates
- Invites for Playdates belongs to both a Profile and My Scheduled Playdate 
- My Scheduled Playdate belong to Profile as Host
- Profile as Host has many My Scheduled Playdates

### Tech Stack:
- Django
- Postgres