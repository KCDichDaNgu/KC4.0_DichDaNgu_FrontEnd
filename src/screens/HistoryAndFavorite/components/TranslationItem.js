import React from 'react';
import { 
	Typography, 
	Card, 
	CardContent, 
	CardActionArea,
	CardActions,
} from '@mui/material';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import ArrowForwardIcon from '@mui/icons-material/ArrowForward';
import StarBorderIcon from '@mui/icons-material/StarBorder';
import IconButton from '@mui/material/IconButton';
import DeleteIcon from '@mui/icons-material/Delete';
import { useTranslation } from 'react-i18next';
import { changeHistory } from '../../../redux/actions/historyAction';

function TranslationItem(props) {
	const {item} = props;
	const { t } = useTranslation();


	const trimText = (text) => {
		const trimText = text.trim();
		return trimText.length > 10 ? text.substring(0,30) + '...' : text;
	};


	const changeCodeToText = (code) => {
		switch (code) {
		case 'en':
			return t('Translate.listLanguage.anh');
		case 'vi':
			return t('Translate.listLanguage.viet');
		case 'zh':
			return t('Translate.listLanguage.trung');
		case 'lo':
			return t('Translate.listLanguage.lao');
		case 'km':
			return t('Translate.listLanguage.khome');
		default:
			return code;
		}
	};

	return (
		<Card variant="outlined" style={{borderRadius: 0}}>
			<CardActionArea onClick={() => props.changeHistory(item)}>
				<CardContent>
					<Typography gutterBottom variant="body2" component="div"> 
						{item ? trimText(item.source_text) : null}
					</Typography>
					<Typography gutterBottom variant="body2" component="div" color="text.secondary">
						{item ? trimText(item.target_text) : null}
					</Typography>
					<Typography variant="body2" color="text.secondary">
						{changeCodeToText(item ? item.source_lang : null)} <ArrowForwardIcon sx={{fontSize: 20}}/> {changeCodeToText(item ? item.target_lang : null)}
					</Typography>
				</CardContent>
			</CardActionArea>
			<CardActions sx={{p: 0}} disableSpacing style={{justifyContent: 'end'}}>
				<IconButton aria-label="directions" id="basic-button" disabled>
					<StarBorderIcon />
				</IconButton>
				<IconButton aria-label="directions" id="basic-button" disabled>
					<DeleteIcon />
				</IconButton>
			</CardActions>
		</Card>
	);
}

TranslationItem.propTypes = {
	item: PropTypes.object,
	changeHistory: PropTypes.func,
};

const mapStateToProps = (state) => ({
	historyState: state.historyReducer,
});


const mapDispatchToProps = { 
	changeHistory
};

export default connect(mapStateToProps, mapDispatchToProps)(TranslationItem);
