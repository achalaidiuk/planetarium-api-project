# Api Planetarium project

API Planetarium is a comprehensive and intuitive platform designed to explore, discover, and understand the vast universe of APIs. Whether you're a seasoned developer or just starting out, API Planetarium provides a stellar experience for navigating through APIs from various domains, allowing you to easily find the right resources for your projects. With interactive visualizations and powerful search capabilities, embark on a journey through the API galaxy and unlock the potential of seamless integration for your applications. Join us in exploring the endless possibilities of the API universe with API Planetarium.

-------------------------------------------------------------------------------------
## Features

- **Astronomy Data**: Access detailed information about astronomy, including astronomical events, and observations.
- **Reservation Management**: Manage reservations for planetarium shows, allowing users to book seats and view their reservation details.
- **Ticketing System**: Handle ticket sales and distribution for planetarium shows, providing options for purchasing tickets online.
- **Show Sessions**: View schedules and timings for planetarium shows, including upcoming sessions, show durations, and availability.
- **Show Themes**: Explore different themes for planetarium shows.
- **Planetarium Dome Configuration**: Access configuration settings for the planetarium dome.

-------------------------------------------------------------------------------------

## API Reference

#### Before start using this API Project, u should use register(if not yet) or use JWT Token for authentification if u already register.

#### For register:

```http
  POST api/user/register/
```
| Key | Type     | Description                |
| :-------- | :------- | :------------------------- |
| Email | Email | Required. Your Email |
| Password | Password | Required. Your Password |

#### For authentification (you should use your credentetials for authentification)

```HTTP
  GET api/user/token/
```
| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| Email    | Email | Required. Your Email |
| Password    | Password | Required. Your Password |

### You can see information about your account inc. email, are you staff etc. (update account info as well)


```HTTP
  GET api/user/me/
```
------------------------------------------------------------------------------------

## RESOURCES

Note: You can get further resources if you are authenticated
 
#### Get list of Show Themes and create new one (if you have admin permissions)

```HTTP
   GET /api/planetarium/show_theme/
```
#### Get list of Show Sessions and create new one (if you have admin permissions)

```HTTP
   GET /api/planetarium/show_session/
```
#### Get list of Planetarium Domes and create new one (if you have admin permissions)

```HTTP
   GET /api/planetarium/planetarium_dome/
```
#### Get list of Astronomy Shows and create new one (if you have admin permissions)

```HTTP
   GET /api/planetarium/astronomy/
```
#### Update current theme (possible if user has admin permissions)
```HTTP
   PUT, PATCH or DELETE /api/planetarium/show_theme/{id: int}/
```
#### Update current show session (possible if user has admin permissions)
```HTTP
   PUT, PATCH or DELETE /api/planetarium/show_session/{id: int}/
```
#### Update current planetarium dome (possible if user has admin permissions)
```HTTP
   PUT, PATCH or DELETE /api/planetarium/planetarium_dome/{id: int}/
```
#### Update current astronomy show (possible if user has admin permissions)
```HTTP
   PUT, PATCH or DELETE /api/planetarium/astronomy/{id: int}/
```
-----------------------------------------------------------------------------------
### Create reservation for you
```HTTP
   GET /api/planetarium/reservation/
```
#### After that you should take a ticket from your reservation

Note: You can see the tickets that only you ordered

### Create reservation for you

```HTTP
   GET /api/planetarium/tickets/
```
----------------------------------------------------------------------------------
## Admin Panel

#### You can join admin panel through this endpoint:
```HTTP
GET /admin
```
*Example*: http://127.0.0.1:8001/admin/

#### Information about superuser:


| *Parameter* | *Type*        | 
| :-------- |:--------------|
| Nickname   | Interjkee     |
| Password    | lokaster52624 |
----------------------------------------------------------------------------------
```