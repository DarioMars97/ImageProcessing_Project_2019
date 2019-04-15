##Image Processing Project 2019
project about bus services in cairo which process is meant to be : 
take an obvious pic of the bus which number is clear and get the user the bus's route or to enter his destination and verify that this bus will get him there or not.

>### This directory is concerned with the server side

### APIs:-

#### list all buses (get)
>https://image-processing-bus-services.herokuapp.com/bus_service/buses

#### add bus (post)
>https://image-processing-bus-services.herokuapp.com/bus_service/buses

body:-
>{"bus_number" : 500}

#### list all zones (get)
>https://image-processing-bus-services.herokuapp.com/bus_service/zones

#### add zone (post)
>https://image-processing-bus-services.herokuapp.com/bus_service/zones

body:-
>{"zone_text" : "El Harram"}

#### list all images (get)
>https://image-processing-bus-services.herokuapp.com/bus_service/upload_image

#### add image (post)
>https://image-processing-bus-services.herokuapp.com/bus_service/upload_image

body:-
>{file : }

#### get zones of a certain bus (get)
>https://image-processing-bus-services.herokuapp.com/bus_service/bus/1003/zones

#### add zone to certain bus (post)
>https://image-processing-bus-services.herokuapp.com/bus_service/bus/1003/zones

body:-
>{"zone_text" : "Imbaba"}
 