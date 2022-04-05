#version 330 core


// Vertex shader



// input attribute variable, given per vertex
layout(location = 0) in vec3 xyz;
layout(location = 1) in vec2 uv;
layout(location = 2) in vec3 nor;
layout(location = 3) in vec3 tng;
layout(location = 4) in vec3 btg;


// input variables from code
uniform mat4 model_matrix;
uniform mat4 view_matrix;
uniform mat4 projection_matrix;
uniform vec3 light_vector;


// output interpolated values for the fragment shader
out vec3 normal_vector;
out vec3 light_direction;
out vec3 eye_vector;
out vec3 tangent_vector;
out vec3 bitangent_vector;
out vec2 texture_coord;


// from each vertex, values will be interpolated
void main()
{
	// first need the view_space_matrix
	// Using the upper 3x3 of the modelview matrix only works with uniforms scales,
	// otherwise have to use the transpose of the inverse of the modelview (which is a 4x4 matrix)
	mat3 view_space_matrix = mat3( view_matrix * model_matrix );
	
	
	// need normalize vector because maybe the matrix scale it
	normal_vector = normalize(view_space_matrix * nor);
	
	// transform all model related vectors to the view-space coordinate system
	// get the vector from vertex to eye by the neg operator
	eye_vector = vec3(0,0,0) - (view_matrix * model_matrix * vec4(xyz,1.0)).xyz;
	
	// for the light_direction need to view_matrix multiplication
	// need normalize vector because maybe the matrix scale it
	light_direction= normalize(mat3(view_matrix) * light_vector) ;
	
	// for TBN matrix transform tangent and bitangent vectors
	tangent_vector   = view_space_matrix*tng ;
	bitangent_vector = view_space_matrix*btg ;
	
	
	texture_coord = uv;
	
	gl_Position = projection_matrix * view_matrix * model_matrix * vec4(xyz, 1.0);
}
