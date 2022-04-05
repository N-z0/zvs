#version 330 core

// Fragment shader
// Simply display 3d faces without any texture



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
//uniform float blend_factor;
uniform vec4 fog;

// receiving interpolated variables from vertex shader
in vec3 normal_vector;
in vec3 light_direction;
in vec3 eye_vector;

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
	// the greater the angle between both vectors, the darker is diffuse component 
	// use the max function that returns zero or higher, to make sure the diffuse component is never negative even if angle between both vectors is greater than 90 degrees
	//   proximity=1 light is at the vertical of the triangle face
	//   proximity=0 light is perpendicular to the triangle face
	//   proximity<0 light is behind the triangle face
	float proximity = max( dot(normal_vector,light_direction) ,0);
	
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
	vec3 ambient = GetAmbientLight(light,material.base.rgb,material.ao);
	vec3 diffuse = GetDiffuseLight(light,material.base.rgb,normal_vector,light_direction);
	vec3 specular = GetSpecularLight(light,normal_vector,light_direction,eye_vector,material.shine);
	vec4 frag_result = vec4( ambient + diffuse + specular , material.base.a );
	
	vec4 object_color = mix( material.emit, vec4(frag_result.rgb,1), frag_result.a );
	
	frag_color = vec4( mix(object_color.rgb,fog.rgb,GetFogFactor(fog.a,eye_vector)) ,object_color.a );
}
