from PIL import Image
import numpy as np

def array_to_img(arr):
	#Convert a numpy array to a PIL image.
	arr = clip_array(arr)
	arr = arr.astype('uint8')
	img = Image.fromarray(arr, mode='RGB')
	return img

def clip_array(arr, min_value=0, max_value=255):
	# clip values to lie in the range [0, 255]
	comp_arr = np.ones_like(arr)
	arr = np.maximum(comp_arr * min_value, arr)
	arr = np.minimum(comp_arr * max_value, arr)
	return arr

def trans_colorspace(img, mat):
	return np.einsum("ij, ...j", mat, img)

def sim_color_blindness(img, deficit = "d"):
	#colorspace transformation matrices
	cb_matrices = {
	  "d": np.array([[1, 0, 0], [0.494207, 0, 1.24827], [0, 0, 1]]),
	  "p": np.array([[0, 2.02344, -2.52581], [0, 1, 0], [0, 0, 1]]),
	  "t": np.array([[1, 0, 0], [0, 1, 0], [-0.395913, 0.801109, 0]]),
	}
	# rgb to lms colorspace conversion
	rgb2lms = np.array([[17.8824, 43.5161, 4.11935],
		               [3.45565, 27.1554, 3.86714],
		               [0.0299566, 0.184309, 1.46709]])
	# Precomputed inverse for lms to rgb
	lms2rgb = np.array([[8.09444479e-02, -1.30504409e-01, 1.16721066e-01],
		               [-1.02485335e-02, 5.40193266e-02, -1.13614708e-01],
		               [-3.65296938e-04, -4.12161469e-03, 6.93511405e-01]])
	img = img.copy()
	img = img.convert('RGB')

	rgb = np.asarray(img, dtype = float)

	lms = trans_colorspace(rgb, rgb2lms)

	simulated_lms = trans_colorspace(lms, cb_matrices[deficit])
	return array_to_img(trans_colorspace(simulated_lms, lms2rgb))

def daltonize(rgb, deficit='d'):
	#Adjust color palette of an image to compensate color blindness.
	sim_rgb = sim_color_blindness(rgb, deficit)
	err2mod = np.array([[0, 0, 0], [0.7, 1, 0], [0.7, 0, 1]])

	# rgb - sim_rgb contains the color information that dichromats
	# cannot see. err2mod rotates this to a part of the spectrum that
	# they can see.

	rgb = rgb.convert('RGB')
	rgb = np.asarray(rgb, dtype = float)
	err = trans_colorspace(rgb - sim_rgb, err2mod)
	dtpn = err + rgb
	return array_to_img(dtpn)


def dalton_run(img):
    original_img = Image.open(img)
    original_img_sim = sim_color_blindness(original_img, "p")
    new_img = daltonize(original_img, "p")
    new_img_sim = sim_color_blindness(new_img, "p")
    original_img_sim.save('/home/jpucilos/flask_website/static/sim2.jpg')
    new_img.save('/home/jpucilos/flask_website/static/daltonized2.jpg')
    new_img_sim.save('/home/jpucilos/flask_website/static/daltonized_sim2.jpg')
    return



