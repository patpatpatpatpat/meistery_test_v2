import React from 'react'
import { DataGrid } from '@material-ui/data-grid'

export default function Output(props) {
	const data = props.data
	if (!data || data === undefined) {
		return null
	}

	const columns = [
		{ field: 'date', headerName: 'Date'},
		{ field: 'product', headerName: 'Product'},
		{ field: 'sales_number', headerName: 'Sales Number'},
		{ field: 'revenue', headerName: 'Revenue'},
	];

	return (
		<div style={{ height: 400, width: '100%' }}>
			<DataGrid rows={data} columns={columns} pageSize={5} checkboxSelection />
		</div>
	)
}
