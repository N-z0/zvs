#version 330 core

// Fragment shader for HUD



// input variables from code
uniform float blend_factor;
uniform vec3 blend_color;

// receiving interpolated variables from vertex shader
in vec2 texture_coord;

// inputs textures
uniform sampler2D bitmap;

// output fragment color for OpenGL
out vec4 frag_color;



void main()
{
	frag_color = vec4(blend_color,blend_factor) * texture(bitmap,texture_coord);
}
