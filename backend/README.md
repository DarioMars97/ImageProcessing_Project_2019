## Image Processing Project 2019
project about bus services in cairo which process is meant to be : 
take an obvious pic of the bus which number is clear and get the user the bus's route or to enter his destination and verify that this bus will get him there or not.

>### This directory is concerned with the server side

### APIs:-

#### list all buses (get)
>https://image-processing-bus-services.herokuapp.com/bus_service/buses

#### add bus (post)
>https://image-processing-bus-services.herokuapp.com/bus_service/buses

body:-
>{"bus_number" : 500, "link" : "https://goo.gl/maps/uYu6nbmJBCrp7qTb7"}

>link here can be neglected

#### list all zones (get)
>https://image-processing-bus-services.herokuapp.com/bus_service/zones

#### add zone (post)
>https://image-processing-bus-services.herokuapp.com/bus_service/zones

body:-
>{"zone_text" : "El Harram"}

#### list all images (get)
>https://image-processing-bus-services.herokuapp.com/bus_service/upload_image

#### upload image and get bus object (post)
>https://image-processing-bus-services.herokuapp.com/bus_service/upload_image

body:-
>{"bus_image" : %%your file%%}

or

>{"bus_image_bytes" : "byte encoded string base64"}

returns:-
>the number OR
>written errors

#### get zones of a certain bus (get)
>https://image-processing-bus-services.herokuapp.com/bus_service/bus/1003/zones

#### add bus object to certain bus (post)
>https://image-processing-bus-services.herokuapp.com/bus_service/bus/1003/zones

body:-
>{"zone_text" : "Imbaba", "link" : "https://goo.gl/maps/uYu6nbmJBCrp7qTb7"}

>can put one of the two
 