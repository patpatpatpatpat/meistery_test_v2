import React from 'react'
import Button from '@material-ui/core/Button'
import Dialog from '@material-ui/core/Dialog'
import DialogActions from '@material-ui/core/DialogActions'
import DialogContent from '@material-ui/core/DialogContent'
import DialogContentText from '@material-ui/core/DialogContentText'

export default function AlertDialog(props) {
	return (
		<div>
			<Dialog
				open={props.openDialog}
				onClose={props.handleCloseDialog}
				aria-labelledby='alert-dialog-title'
				aria-describedby='alert-dialog-description'
			>
				<DialogContent>
					<DialogContentText id='alert-dialog-description'>
						Are you sure you want to replace the data
					</DialogContentText>
				</DialogContent>
				<DialogActions>
					<Button onClick={props.handleCloseDialog} color='primary'>
						No
					</Button>
					<Button onClick={props.handleAccept} color='primary' autoFocus>
						Yes
					</Button>
				</DialogActions>
			</Dialog>
		</div>
	)
}
