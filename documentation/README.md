# Documentation

## Table of contents
 * [Use cases](#use-cases)
   + [Admin](#admin)
   + [User](#user)
     - [Browse channels](#login-and-browse-channels)
     - [Manage threads](#manage-threads)
     - [Messaging](#messaging)
 * [Data model](#data-model)
    + [Class diagram](#class-diagram)
    + [Database schema](#database-schema)

## Use cases

### Admin
- [ ] The administrator can add and delete channels (discussion boards).
- [ ] The administrator can create a secret channel and determine which users have access to that channel.

<img src="./img/use-cases/admin.png">

### User

#### Login and browse channels
- [ ] Users can log in, out, sign up.
- [ ] The user sees a list of channels on the front page of the application.
- [ ] The list of channels contains the number of threads and messages in each channel and the time of the last message sent.

<img src="./img/use-cases/user-browse.png">

#### Manage threads
- [ ] The user can create a new thread in the area by entering the thread title and the content of first message.
- [ ] The user can edit the title of the thread he has created.
- [ ] The user can delete the thread he has created.

<img src="./img/use-cases/user-threads.png">


#### Messaging
- [ ] The user can search for all messages.
- [ ] The user can write a new message to an existing thread.
- [ ] The user can edit the content of the message he has sent.
- [ ] The user can delete the message he has sent.

<img src="./img/use-cases/user-msg.png">

## Data model

### Class diagram
<img src="./img/data/class.png">

### Database schema
This diagram was generated from [this file](./database-diagram.txt) using [dbdiagram.io](dbdiagram.io) and
can be found [online](https://dbdiagram.io/d/60b2812bb29a09603d171c27).
<img src="./img/data/database.png">

