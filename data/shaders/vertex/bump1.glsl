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
out vec3 tbn_normal_vector;
out vec3 tbn_light_direction;
out vec3 tbn_point_of_view;
out vec2 texture_coord;


// from each vertex, values will be interpolated
void main()
{
	// first need the view_space_matrix
	// Using the upper 3x3 of the modelview matrix only works with uniforms scales,
	// otherwise have to use the transpose of the inverse of the modelview (which is a 4x4 matrix)
	mat3 view_space_matrix = mat3( view_matrix * model_matrix );
	
	//
	vec3 normal_vector = normalize(view_space_matrix * nor);
	
	// transform all model related vectors to the view-space coordinate system
	// get the vector from vertex to eye by the neg operator
	vec3 eye_vector = vec3(0,0,0) - (view_matrix * model_matrix * vec4(xyz,1.0)).xyz;
	
	// for the light_direction need to view_matrix multiplication
	vec3 light_direction= normalize(mat3(view_matrix) * light_vector) ;
	
	// for TBN matrix transform tangent and bitangent vectors
	vec3 tangent_vector   = normalize(view_space_matrix*tng) ;
	vec3 bitangent_vector = normalize(view_space_matrix*btg) ;
	
	// for TBN matrix get a 3rd vector perpendicular of tangent and bitangent plan.
	// the crossproduct of two normalized perpendicular vectors is an normalized vector.
	vec3 up_vector = normalize(cross(tangent_vector,bitangent_vector));
	
	// make TBN matrix (tangent,bitangent,normal/up_vector)
	// In standard 3x3 identity matrix the top row contains the X axis, the middle the Y axis and the bottom the Z axis.
	// need inverse of the TBN matrix to transform all relevant world-space vectors to the tangent space.
	// using the transpose function instead of the inverse function.
	// the transpose of an orthogonal matrix equals its inverse. This is a great property as inverse is expensive and a transpose isn't.
	mat3 tbn_matrix = transpose( mat3(tangent_vector, bitangent_vector, up_vector) );
	
	// The view-space vectors are multiplied by the TBN matrix.
	// The vectors goes from 'view-space' to 'tangent-space'
	// We can use this to compute the light direction and the eye direction in tangent-space
	tbn_normal_vector = normalize( tbn_matrix * normal_vector );
	tbn_point_of_view = tbn_matrix * eye_vector;
	tbn_light_direction = normalize(tbn_matrix * light_direction);
	
	
	texture_coord = uv;
	
	gl_Position = projection_matrix * view_matrix * model_matrix * vec4(xyz, 1.0);
}
