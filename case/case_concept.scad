module base() {
    difference() {
        cube([150,100,70]);
        polyhedron(
            points=[[150,100,0],
                    [0,100,0],
                    [150,100,56],
                    [0,100,56],
                    [150,20,0],
                    [0,20,0]],
            faces=[[0,4,2],
                    [1,3,5],
                    [0,2,1],
                    [1,2,3],
                    [5,4,0],
                    [0,1,5],
                    [2,5,3],
                    [2,4,5]]);
    }
}

module logo1() {
    translate([75,50,70])
    linear_extrude(10,center=true)
    resize([130,0,0], auto=true)
    import("/home/hamza/Documents/EURECOM-1A/project_s5/visuwalk/case/logo1.svg",center=true);
}

//not working
module logo2() {
    rotate([90,0,0])
    translate([145,100,65])
    resize([130,50,100], auto=true)
    import("/home/hamza/Documents/EURECOM-1A/project_s5/visuwalk/case/logo2.svg", center=true);
}


difference() {
    base();
    logo1();
    logo2();
}
