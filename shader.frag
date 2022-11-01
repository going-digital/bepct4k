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

float wball;
float wgnd;
float w(vec3 p) {
    vec3 bp = p;
    bp.xz *= bm;
    bp.yz *= bm;
    float box = box3(bp, vec3(.5));
    float phase = t/8., ph = fract(phase);
    phase = floor(phase) + mix(ph, ph * ph, step(32., t));
    wball = length(rep3(p, vec3(.4 + .1 * sin(phase * PI2)))) - .15;
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
