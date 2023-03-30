sorts

    #location = {college_of_business_administration, the_republic, the_holly, indiana_village, international_cultural_center, holden_hall, student_union_building, university_library, student_recreation_center, student_wellness_center}.
    #route_number = {41, 42, 48}.
    #bus_map = {college_of_business_administration___the_republic___the_holly___indiana_village___international_cultural_center, college_of_business_administration___holden_hall___student_union_building___university_library___student_recreation_center___student_wellness_center, college_of_business_administration___student_wellness_center___student_recreation_center___university_library___student_union_building___holden_hall}.

predicates
    % route(X, Y) denotes X is the route number of route Y.
    route(#route_number, #location).
    
    % same_route(X, Y) denotes X and Y are in the same route.
    same_route(#location, #location).
    
    % neighbouring_route(X, Y) denotes X is the neighbouring route of Y if X and Y are in same route
    neighbouring_route(#location, #location).
    
    % previous_route(X, Y) denotes X is the previous route of Y.
    previous_route(#location, #location).
    
    % next_route(X, Y) denotes X is the next_route of Y if X and Y are in the same route.
    next_route(#location, #location).

    % center_point_route(X) denote X is the center point of the route.
    center_point_route(#location).
    
    % starting_route(X, Y) denotes X is the starting route of Y.
    starting_route(#route_number, #location).
    
    % ending_route(X, Y) denotes X is the ending route of Y.
    ending_route(#route_number, #location).
    
    % fastest_route(X, Y) denotes X is the fastest route of Y.
    fastest_route(#location, #route_number, #bus_map).
    
    % bus_route(X, Y) denotes X is the bus route of Y.
    bus_route(#route_number, #bus_map).

rules
    
    % Route 48 locations
    route(48, college_of_business_administration).
    route(48, the_republic).
    route(48, the_holly).
    route(48, indiana_village).
    route(48, international_cultural_center).
    
    % Route 42 locations
    route(42, college_of_business_administration).
    route(42, holden_hall).
    route(42, student_union_building).
    route(42, university_library).
    route(42, student_recreation_center).
    route(42, student_wellness_center).
    
    % Route 41 locations
    route(41, college_of_business_administration).
    route(41, student_wellness_center).
    route(41, student_recreation_center).
    route(41, university_library).
    route(41, student_union_building).
    route(41, holden_hall).

    % Center Point of every route
    center_point_route(college_of_business_administration, 41).
    center_point_route(college_of_business_administration, 42).
    center_point_route(college_of_business_administration, 43).
    
    % Starting Location of each route
    starting_route(college_of_business_administration, 41).
    starting_route(college_of_business_administration, 42).
    starting_route(college_of_business_administration, 48).
    
    % Ending Location of each route
    ending_route(holden_hall, 41).
    ending_route(student_wellness_center, 42).
    ending_route(international_cultural_center, 48).
    
    % Next Route for 48
    next_route(college_of_business_administration, international_cultural_center).
    next_route(international_cultural_center, indiana_village).
    next_route(indiana_village, the_holly).
    next_route(the_holly, the_republic).
    next_route(the_republic, college_of_business_administration).
    
    % Next Route for 42
    next_route(college_of_business_administration, student_wellness_center).
    next_route(student_wellness_center, student_recreation_center).
    next_route(student_recreation_center, university_library).
    next_route(university_library, student_union_building).
    next_route(student_union_building, holden_hall).
    next_route(holden_hall, college_of_business_administration).
    
    % Next Route for 41
    next_route(college_of_business_administration, holden_hall).
    next_route(holden_hall, student_union_building).
    next_route(student_union_building, university_library).
    next_route(university_library, student_recreation_center).
    next_route(student_recreation_center, student_wellness_center).
    next_route(student_wellness_center, college_of_business_administration).
    
    
    % Previous Route for 48
    previous_route(college_of_business_administration, the_republic).
    previous_route(the_republic, the_holly).
    previous_route(the_holly, indiana_village).
    previous_route(indiana_village, international_cultural_center).
    previous_route(international_cultural_center, college_of_business_administration).
    
    % Previous Route for 42
    previous_route(college_of_business_administration, holden_hall).
    previous_route(holden_hall, student_union_building).
    previous_route(student_union_building, university_library).
    previous_route(university_library, student_recreation_center).
    previous_route(student_recreation_center, student_wellness_center).
    previous_route(student_wellness_center, college_of_business_administration).
    
    % Previous Route for 41
    previous_route(college_of_business_administration, student_wellness_center).
    previous_route(student_wellness_center, student_recreation_center).
    previous_route(student_recreation_center, university_library).
    previous_route(university_library, student_union_building).
    previous_route(student_union_building, holden_hall).
    previous_route(holden_hall, college_of_business_administration).
    
    % Bus Route
    bus_route(41, college_of_business_administration___student_wellness_center___student_recreation_center___university_library___student_union_building___holden_hall).
    bus_route(42, college_of_business_administration___holden_hall___student_union_building___university_library___student_recreation_center___student_wellness_center).
    bus_route(48, college_of_business_administration___the_republic___the_holly___indiana_village___international_cultural_center).
    
    % Fastest Route for X to Y
     
    % Fastest Route for X to Y
    fastest_route(college_of_business_administration___the_republic___the_holly___indiana_village___international_cultural_center, the_republic).
    fastest_route(college_of_business_administration___the_republic___the_holly___indiana_village___international_cultural_center, the_holly).
    fastest_route(college_of_business_administration___the_republic___the_holly___indiana_village___international_cultural_center, indiana_village).
    fastest_route(college_of_business_administration___the_republic___the_holly___indiana_village___international_cultural_center, international_cultural_center).
    fastest_route(college_of_business_administration___holden_hall___student_union_building___university_library___student_recreation_center___student_wellness_center, holden_hall).
    fastest_route(college_of_business_administration___holden_hall___student_union_building___university_library___student_recreation_center___student_wellness_center, student_union_building).
    fastest_route(college_of_business_administration___holden_hall___student_union_building___university_library___student_recreation_center___student_wellness_center, university_library).
    fastest_route(college_of_business_administration___student_wellness_center___student_recreation_center___university_library___student_union_building___holden_hall, university_library).
    fastest_route(college_of_business_administration___student_wellness_center___student_recreation_center___university_library___student_union_building___holden_hall, student_recreation_center).
    fastest_route(college_of_business_administration___student_wellness_center___student_recreation_center___university_library___student_union_building___holden_hall, student_wellness_center).
    
    % Not Same Route
    -same_route(X,Y) :- not same_route(X,Y).
    
    % Same Route
    same_route(X,Y) :- route(Z, X), route(Z, Y), X != Y.
    
    % Next Route
    next_route(X,Y) :- next_route(X, Y).
    
    % Not Next Route
    -next_route(X,Y) :- not next_route(X, Y).
    
    % Neighbour Route
    neighbouring_route(X, Y) :- next_route(X, Y).
    
    neighbouring_route(X, Y) :- previous_route(X, Y).
    
    % Not Neighbour Route
    -neighbouring_route(X, Y) :- not next_route(X, Y).
    
    -neighbouring_route(X, Y) :- not previous_route(X, Y).