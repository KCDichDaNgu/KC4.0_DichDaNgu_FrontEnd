import React from 'react';
import PropTypes from 'prop-types';
import { Zoom } from '@mui/material';
import Box from '@mui/material/Box';
import useScrollTrigger from '@mui/material/useScrollTrigger';

export default function ScrollTop(props) {
	const { children } = props;

	const trigger = useScrollTrigger({
		disableHysteresis: true,
		threshold: 100,
	});
  
	const handleClick = () => {
		window.scrollTo(0, 0);
	};
  
	return (
		<Zoom in={trigger}>
			<Box onClick={handleClick} role="presentation" sx={{ position: 'fixed', bottom: 16, right: 16 }}>
				{children}
			</Box>
		</Zoom>
	);
}
  
ScrollTop.propTypes = {
	children: PropTypes.element.isRequired,
};