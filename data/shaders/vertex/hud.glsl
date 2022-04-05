#version 330 core

// Vertex shader for HUD



// input attribute variable, given per vertex
layout(location = 0) in vec3 xyz;
layout(location = 1) in vec2 uv;

// input variables from code
uniform mat4 model_matrix;
uniform mat4 projection_matrix;

// output interpolated values for the fragment shader
out vec2 texture_coord;



// from each vertex, values will be interpolated
void main()
{
	texture_coord = uv;
	gl_Position = projection_matrix * model_matrix * vec4(xyz, 1.0);
}
