sorts

    #location = {college_of_business_administration, the_republic, the_holly, indiana_village, international_cultural_center, holden_hall, student_union_building, university_library, student_recreation_center, student_wellness_center}.
    #route_number = {41, 42, 48}.

predicates
    % route(X, Y) denotes X is the route number of route Y.
    route(#route_number, #location).
    
    % same_route(X, Y) denotes X and Y are in the same route.
    same_route(#location, #location).
    
    % neighbouring_route(X, Y) denotes X is the neighbouring route of Y if X and Y are in same route
    
    % next_route(X, Y) denotes X is the next_route of Y if X and Y are in the same route.
    next_route(#location, #location).

    center_point_route(#location).
    
    starting_route(#location, #route_number).
    
    ending_route(#location, #route_number).

rules

    route(48, college_of_business_administration).
    route(48, the_republic).
    route(48, the_holly).
    route(48, indiana_village).
    route(48, international_cultural_center).
    route(42, holden_hall).
    route(42, student_union_building).
    route(42, university_library).
    route(42, student_recreation_center).
    route(42, student_wellness_center).
    
    center_point_route(college_of_business_administration).
    
    starting_route(college_of_business_administration, 41).
    starting_route(college_of_business_administration, 42).
    starting_route(college_of_business_administration, 48).
    
    ending_route(holden_hall, 41).
    ending_route(student_wellness_center, 42).
    ending_route(international_cultural_center, 48).
    
    % Next Route for 48
    next_route(college_of_business_administration, the_republic).
    next_route(the_republic, the_holly).
    next_route(the_holly, indiana_village).
    next_route(indiana_village, international_cultural_center).
    next_route(international_cultural_center, college_of_business_administration).
    
    % Next Route for 42
    next_route(college_of_business_administration, holden_hall).
    next_route(holden_hall, student_union_building).
    next_route(student_union_building, university_library).
    next_route(university_library, student_recreation_center).
    next_route(student_recreation_center, student_wellness_center).
    next_route(student_wellness_center, college_of_business_administration).
    
    % 
    
    -same_route(X,Y) :- not route(Z, X), route(Z, Y), X != Y.
    same_route(X,Y) :- route(Z, X), route(Z, Y), X != Y.
    
    next_route(X,Y) :- next_route(X, Y).