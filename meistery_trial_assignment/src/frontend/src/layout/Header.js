import React from 'react'
import clsx from 'clsx'
import AppBar from '@material-ui/core/AppBar'
import Toolbar from '@material-ui/core/Toolbar'
import Typography from '@material-ui/core/Typography'
import useStyles from './Style'

const Header = () => {
	const classes = useStyles()
	return (
		<AppBar
			position='absolute'
			className={clsx(classes.appBar)}
		>
			<Toolbar className={classes.toolbar}>
				<Typography
					component='h1'
					variant='h6'
					color='inherit'
					noWrap
					className={classes.title}
				>
					React Web App
				</Typography>
			</Toolbar>
		</AppBar>
	)
}

export default Header
