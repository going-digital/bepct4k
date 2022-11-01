uniform float t;

float hash2(vec2 v) {
    return fract(
        sin(
            dot(v, vec2(37.467,63.534))
        ) * 68354.452
    );
} 

const vec3 E = vec3(.0, .001, 1.);

float noise2(vec2 v) {
    vec2 V=floor(v);
    v -= V;
    v *= v * (3. - 2. * v);
    return mix(
        mix(hash2(V), hash2(V + E.zx), v.x),
        mix(hash2(V + E.xz), hash2(V + E.zz), v.x),
        v.y
    );
}

const float PI = 3.1415926, PI2 = PI+PI;

vec3 iqcolor(vec3 a, vec3 b, vec3 c, vec3 d, float t) {
    return a + b * cos(PI2 * (c + t * d));
}

vec3 c1(float t) {
	return iqcolor(
        vec3(.5),
        vec3(.5),
        vec3(1.),
        vec3(0., 0.33, 0.67),
        t
    );
}

vec3 rep3(vec3 p, vec3 s) {
    return mod(p, s) - s * .5;
}

float vmax(vec3 p) {
    return max(max(p.x, p.y), p.z);
}
float box3(vec3 p, vec3 s) {
    return vmax(abs(p) - s);
}

mat2 Rm(float a) {
    //float c=cos(a), s=sin(a);
    //return mat2(c,s,-s,c);
    return mat2(cos(a+vec4(0,11,33,0)));
}

mat2 bm;
float bunny(vec3 p){
  return -.428
    + .332*length(p-.01*vec3(64,-44,35))
    - .359*length(p-.01*vec3(0,-2,29))
    + .285*length(p-.01*vec3(53,-45,-63))
    + .231*length(p-.01*vec3(44,1,-54))
    + .187*length(p-.01*vec3(44,0,-54))
    - .832*length(p-.01*vec3(10,-5,-79))
    + .255*length(p-.01*vec3(37,-30,-52))
    + .066*length(p-.01*vec3(4,-8,-7))
    - .417*length(p-.01*vec3(41,-15,12))
    + .159*length(p-.01*vec3(-59,7,0))
    + .658*length(p-.01*vec3(-25,-40,46))
    - .158*length(p-.01*vec3(44,-16,-31))
    + .245*length(p-.01*vec3(7,-4,-14))
    + .158*length(p-.01*vec3(8,36,24))
    + .579*length(p-.01*vec3(-67,-27,45))
    - .246*length(p-.01*vec3(38,-69,-37))
    - .403*length(p-.01*vec3(-25,-31,-36))
    - .27*length(p-.01*vec3(-27,-55,18))
    + .42*length(p-.01*vec3(40,-44,20))
    + .152*length(p-.01*vec3(6,-5,-13))
    + .255*length(p-.01*vec3(46,43,48))
    - .183*length(p-.01*vec3(-21,-14,33))
    - .174*length(p-.01*vec3(37,-14,18))
    + .403*length(p-.01*vec3(-21,-11,-54))
    + .152*length(p-.01*vec3(-35,-1,-8))
    + .283*length(p-.01*vec3(-17,-48,-10))
    + .503*length(p-.01*vec3(-1,-41,-58))
    - .29*length(p-.01*vec3(-49,-1,28))
    - .362*length(p-.01*vec3(20,1,44))
    + .32*length(p-.01*vec3(-1,-12,49))
    - .342*length(p-.01*vec3(-70,12,31))
    + .257*length(p-.01*vec3(28,-32,42))
    + .229*length(p-.01*vec3(13,69,-41))
    + .232*length(p-.01*vec3(44,4,-11))
    - .425*length(p-.01*vec3(7,23,52))
    - .285*length(p-.01*vec3(-28,-32,17))
    + .09*length(p-.01*vec3(5,-7,-9))
    + .063*length(p-.01*vec3(3,27,18))
    + .259*length(p-.01*vec3(13,69,-41))
    - .272*length(p-.01*vec3(47,-19,-32))
    - .287*length(p-.01*vec3(-64,-26,6))
    - .31*length(p-.01*vec3(-3,51,62))
    + .193*length(p-.01*vec3(6,-5,-12))
    + .304*length(p-.01*vec3(37,-30,-52))
    - .394*length(p-.01*vec3(-23,-75,34))
    + .189*length(p-.01*vec3(7,-4,-14))
    - .516*length(p-.01*vec3(3,-40,73))
    - .503*length(p-.01*vec3(-35,-13,71))
    - .386*length(p-.01*vec3(-25,-22,71))
    - .258*length(p-.01*vec3(78,-40,-24))
    - .457*length(p-.01*vec3(-33,-6,33))
    - .394*length(p-.01*vec3(19,-7,34))
    - .358*length(p-.01*vec3(-22,-13,34))
    - .358*length(p-.01*vec3(13,-52,-38))
    + .212*length(p-.01*vec3(-0,32,19))
    + .661*length(p-.01*vec3(-5,-5,56))
    + .843*length(p-.01*vec3(-17,6,61))
    + .022*length(p-.01*vec3(3,-5,-5))
    - .401*length(p-.01*vec3(-27,-21,-33))
    + .245*length(p-.01*vec3(20,18,22))
    + .742*length(p-.01*vec3(-26,18,76))
    - .139*length(p-.01*vec3(44,-15,-31))
    - .336*length(p-.01*vec3(45,22,67))
    + .147*length(p-.01*vec3(34,21,34))
    - .285*length(p-.01*vec3(66,-7,35))
    - .232*length(p-.01*vec3(-83,-56,-20))
    + .535*length(p-.01*vec3(-40,-37,53))
    + .094*length(p-.01*vec3(5,-9,-7))
    - .381*length(p-.01*vec3(-30,-15,59))
    + .313*length(p-.01*vec3(-38,-24,-67))
    - .291*length(p-.01*vec3(-18,29,37))
    + .621*length(p-.01*vec3(-47,-37,65))
    + .325*length(p-.01*vec3(13,-40,-10))
    - .179*length(p-.01*vec3(-98,70,22))
    - .271*length(p-.01*vec3(45,-17,-31))
    - .16*length(p-.01*vec3(85,99,-29))
    + .155*length(p-.01*vec3(-56,-4,-5))
    + .455*length(p-.01*vec3(16,-45,36));
}

float wball;
float wgnd;
float w(vec3 p) {
    vec3 bp = p;
    bp.xz *= bm;
    bp.yz *= bm;
    float box = bunny(bp);//box3(bp, vec3(.5));
    float phase = t/8., ph = fract(phase);
    phase = floor(phase) + mix(ph, ph * ph, step(32., t));
    wball = length(rep3(p, vec3(.3 + .1 * sin(phase * PI2)))) - .15;
    float h = noise2(p.xz) + .25 * noise2(p.xz * 2.3+vec2(t));
    wgnd = p.y + .5 + h * h;
    return min(max(wball, box), wgnd);
}

vec3 wn(vec3 p) {
    return normalize(
        vec3(
            w(p+E.yxx), w(p+E.xyx), w(p+E.xxy)
        ) - w(p)
    );
}

void main() {
    vec2 uv = (gl_FragCoord.xy-vec2(960,540))/1080.;
    
    bm = Rm(t/4.);

	vec3 skycolor = vec3(.4, .7, .9);
    vec3 C = skycolor;
  
    mat2 mc = Rm(.2), mc2 = Rm(t/8.);
    vec3 O = vec3(0., 0., 3.);
    vec3 D = normalize(vec3(uv, -2.));
   	O.yz *= mc; D.yz *= mc;
    O.xz *= mc2; D.xz *= mc2;
    
    float L = 10.;
    float i, d, l = 0.;
    float Ni = 200.;
    vec3 P;
    for (i = 0.; i < Ni; ++i) {
        P = O + D * l;
        d = w(P);
        l += d * .6;
        if (d < .001 * l || l > L) break;
    }

    if (l < L) {
        float spec = 25.;
        vec3 alb = vec3(1.);
        
        if (d == wgnd) {
            alb = c1(P.y - 3.);
        }
        
        vec3 N = wn(P);
        
        vec3 sundir = normalize(vec3(1.));
       	vec3 h = normalize(sundir-D);

        vec3 suncolor = vec3(.9, .8, .5);
        vec3 c = suncolor * alb * (
           max(0., dot(N, sundir)) + pow(max(0., dot(N, h)), spec)
        );
        
        c += alb * skycolor * max(N.y, 0.);
        c += 2. * i/Ni;
        C = mix(C,c, smoothstep(L, L*.5, l));
    }

    // Fade in
    C *= pow(smoothstep(0., 32., t), 2.);

    // Output to screen

    // Apply Gamma 2.0
    gl_FragColor.rgb = sqrt(C);

    // or Apply ACES Filmic (costs about 13 bytes extra)
    // Krysztof Narkowicz's curve fit
    // https://knarkowicz.wordpress.com/2016/01/06/aces-filmic-tone-mapping-curve/
    //gl_FragColor.rgb = (C * (C * 2.51 + .03)) / (C * (C * 2.43 + .59) + .14);

}
