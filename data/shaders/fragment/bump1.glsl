#version 330 core

// Fragment shader
// 
// 
// 



// input structures
struct Light {
	vec3 ambient;
	vec3 diffuse;
};

struct Material {
	vec4 emit;
	vec4 base;
	float shine;
	float ao;
};

// input variables from code
uniform Light light;
uniform Material material;
uniform float blend_factor;
uniform vec4 fog;

// receiving interpolated variables from vertex shader
in vec3 tbn_normal_vector;// good +x=r vers les trolls, +y=g seloigant
in vec3 tbn_light_direction;
in vec3 tbn_point_of_view;// good +x=r vers les trolls, +y=g seloigant
in vec2 texture_coord;

// input textures
uniform sampler2D emissive_texture;
uniform sampler2D ao_texture;
uniform sampler2D base_texture;
uniform sampler2D highlight_texture;
uniform sampler2D metal_texture;
uniform sampler2D normal_texture;

// output fragment color for OpenGL
out vec4 frag_color;



vec3 VectorToColor(vec3 vector)
{
	return (vector + 1) / 2;
}
vec3 ColorToVector(vec3 color)
{
	return color * 2 - 1.0 ;
}


vec3 GetAmbientLight(Light light,vec3 color,float occlusion)
{
	return ( light.ambient * color * occlusion);
}

vec3 GetDiffuseLight(Light light,vec3 color,vec3 normal_vector,vec3 light_direction)
{
	// negate the light.direction vector because need to be from the fragment towards the light source
	// also normalize the vector because its unwise to assume the input vector is unit vector
	vec3 light_dir = normalize( light_direction );
	
	// the greater the angle between both vectors, the darker is diffuse component 
	// use the max function that returns zero or higher, to make sure the diffuse component is never negative even if angle between both vectors is greater than 90 degrees
	//   proximity=1 light is at the vertical of the triangle face
	//   proximity=0 light is perpendicular to the triangle face
	//   proximity<0 light is behind the triangle face
	float proximity = max( dot(normal_vector,light_dir) ,0);
	
	//result
	return ( light.diffuse * proximity * color );
}

vec3 GetSpecularLight(Light light,vec3 normal_vector,vec3 light_direction,vec3 point_of_view,float shininess)
{	
	// Specular Blinn-Phong shading introduced in 1977 by James F. Blinn
	// The Blinn-Phong shading model was the exact shading model used in the earlier fixed function pipeline of OpenGL.
	
	vec3 pov_vector = normalize(point_of_view);
	vec3 middle_vector = normalize(light_direction + pov_vector);
	float angle = max( dot(normal_vector,middle_vector) ,0);
	//float shine = pow( angle, shininess);// shininess=0 shine=1 , shininess=1 shine=angle
	float shine = pow( angle, shininess*1000);// normally range from 0 to 1000
	
	return ( light.diffuse * shine );//
	//return ( light.diffuse * shininess * shine );//
}


float GetFogFactor(float factor,vec3 point_of_view)
{
	// the attenuation caused by fog or smoking is never linear in real world.
	// make sure it will not be grater than 1
	return ( min(pow(length(point_of_view),2)*factor,1) );
}


void main()
{
	// obtain tangent space normal from normal map
	// The normal is stored as a color so its components are in the range [0-1]
	// We transform it back to its original range [-1,1]
	vec3 tex_normal= normalize( ColorToVector(texture(normal_texture,texture_coord).rgb) );
	vec3 frag_normal= normalize( mix( tbn_normal_vector, tex_normal, blend_factor) );
	
	vec4 frag_emit= mix( material.emit, texture(emissive_texture,texture_coord), blend_factor);
	float frag_ao= mix( material.ao, texture(ao_texture,texture_coord).r, blend_factor);
	vec4 frag_diffus= mix( material.base, texture(base_texture,texture_coord), blend_factor);
	float frag_highlight= mix( material.shine, texture(highlight_texture,texture_coord).r, blend_factor);
	
	vec3 ambient = GetAmbientLight(light,frag_diffus.rgb,frag_ao);
	vec3 diffuse = GetDiffuseLight(light,frag_diffus.rgb,frag_normal,tbn_light_direction);
	vec3 specular = GetSpecularLight(light,frag_normal,tbn_light_direction,tbn_point_of_view,frag_highlight);
	vec4 frag_result = vec4( ambient + diffuse + specular , frag_diffus.a );
	
	vec4 object_color = mix( frag_emit, vec4(frag_result.rgb,1), frag_result.a );
	
	//frag_color = vec4( mix(object_color.rgb,fog.rgb,GetFogFactor(fog.a,tbn_point_of_view)) ,object_color.a );
	frag_color = vec4(diffuse,1);
}
