width = 70;
depth = 55;
height = 95;
camera_orientation = 25; // camera angle orientation in degrees

screw_d = 4; // screw hole diameter

base_depth = 25;
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
    translate([width/2,depth,(height+hole_height)/2])
    rotate([90,0,180])
    linear_extrude(10,center=true)
    resize([0.75*width,0,0], auto=true)
    import("/home/hamza/Documents/EURECOM-1A/visuwalk/case/logo1.svg",center=true);
}

module logo2() {
    module txt(){text("visuwalk", size=0.1*width,font="URW Gothic:style=Demi");}
    translate([0.78*width,depth,hole_height+10])
    rotate([90,0,180])
    linear_extrude(10,center=true)
    txt();
}

module braille() {
    module txt(){text("⠧⠊⠎⠥⠺⠁⠇⠅", size=0.07*width,font="Braille");}
    translate([0.55*width,depth,height-10])
    rotate([90,0,180])
    linear_extrude(1,center=true)
    txt();
}

module case() {
    union() {
        difference() {
            base();
            logo1();
            logo2();
            translate([-1,2,height-1]) cube([width+2,10,2]);
        }
        braille();
    }
}


module arceau() {
    module entier() {
        union() {
            rotate([90,0,0])
            translate([width/2,0.8*height+2.5,0])
            linear_extrude(5)
            square([0.7*width,5],center=true);
            
            rotate([90,0,-90])
            translate([0,0,-0.35*width])
            translate([5,0.8*height,-width/2])
            rotate_extrude(angle=90, convexity=2)
            square([5,0.7*width]);
            
            rotate([180,0,90])
            translate([-7.5,width/2,-0.8*height])
            linear_extrude(50)
            square([5,0.7*width],center=true);
        }
    }
    
    difference() {
        entier();
        scale([0.5,1,1]) translate([35,0,0]) entier(); //magic value here for translate
    }
}

union() {
    case();
    arceau();
}
