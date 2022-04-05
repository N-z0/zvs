#version 330 core

// Vertex shader
// Simply display 3d faces without any texture



// input attribute variable, given per vertex
layout(location = 0) in vec3 xyz;
layout(location = 1) in vec2 uv;
layout(location = 2) in vec3 nor;


// input variables from code
uniform mat4 model_matrix;
uniform mat4 view_matrix;
uniform mat4 projection_matrix;
uniform vec3 light_vector;


// output interpolated values for the fragment shader
out vec3 normal_vector;
out vec3 light_direction;
out vec3 eye_vector;


// from each vertex, values will be interpolated
void main()
{
	
	// need normalize vector because maybe the matrix scale it
	normal_vector = normalize(mat3( view_matrix ) * mat3( model_matrix ) * nor);
	
	// get the vector from vertex to eye by the neg operator
	eye_vector = vec3(0,0,0) - (view_matrix * model_matrix * vec4(xyz,1.0)).xyz;
	
	// need normalize vector because maybe the matrix scale it
	light_direction= normalize(mat3(view_matrix) * light_vector) ;
	
	
	gl_Position = projection_matrix * view_matrix * model_matrix * vec4(xyz, 1.0);
}
