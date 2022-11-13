width = 150;
depth = 100;
height = 70;
camera_orientation = 25; // camera angle orientation in degrees

base_depth = 20;
hole_height = tan(camera_orientation)*(depth-base_depth);
echo("Hole height", hole_height);

module base() {
    difference() {
        cube([width,depth,height]);
        polyhedron(
            points=[[width,depth,0],
                    [0,depth,0],
                    [width,depth,hole_height],
                    [0,depth,hole_height],
                    [width,base_depth,0],
                    [0,base_depth,0]],
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
    translate([width/2,depth/2,height])
    linear_extrude(10,center=true)
    resize([0.75*width,0,0], auto=true)
    import("/home/hamza/Documents/EURECOM-1A/project_s5/visuwalk/case/logo1.svg",center=true);
}

module logo2() {
    module txt(){text("visuwalk", size=0.3*(height-hole_height),font="URW Gothic:style=Demi");}
    rotate([90,0,180])
    translate([-0.95*width,hole_height+5,depth])
    linear_extrude(10,center=true)
    difference(){
        txt();
        offset(delta=-1) txt();
    }
}

difference() {
    base();
    logo1();
    logo2();
}
