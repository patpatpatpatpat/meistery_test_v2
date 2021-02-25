import React from 'react'
import CssBaseline from '@material-ui/core/CssBaseline'
import Container from '@material-ui/core/Container'
import useStyles from './Style'
import Header from './Header'

const Layout = (props) => {
	const classes = useStyles()
	return (
		<div className={classes.root}>
			<CssBaseline />
			<Header />
			<main className={classes.content}>
				<div className={classes.appBarSpacer} />
				<Container maxWidth='lg' className={classes.container}>
					{props.children}
				</Container>
			</main>
		</div>
	)
}

export default Layout
