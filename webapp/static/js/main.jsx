class ProdcutPg extends React.Component {
	state = {
		selectedProduct: null
	}
	onProductSelection(product) {console.log('product', product)
		this.setState({selectedProduct: product});
	}
	render() {
		return <div>
			<h1>Product details</h1>
			<div className="left">
				<ProductsList selectProduct={this.onProductSelection.bind(this)} />
			</div>
			<div className="right">
				<ProductDetail product={this.state.selectedProduct} />
			</div>
			<div className="clearfix"></div>
		</div>;
	}
}

class ProductsList extends React.Component {
	state = {
	    products: []
	  }
	componentWillMount() {
		jQuery.get('/api/products', (data) => {
			this.setState({products: data});
		})
	}
	render() {
		let products = '';
		if (this.state.products) {
			products = this.state.products.map((p) => (<li key={p.product_name} onClick={() => this.props.selectProduct(p)}>{p.product_name}</li>));
		}
		return <div>
			<ol>
				{products}
			</ol>
		</div>;
	}
}

class ProductDetail extends React.Component {
	render() {
		const product = this.props.product;
		if (product)
			return <div>
				<h3>Details</h3><br/>
				Name: {product.product_name}<br/>
				Price: {product.price}<br/>
				ratings: {product.avg_ratings}<br/>
			</div>;
		else
			return <div><p>Please click on a Product name in the list</p></div>;
	}
}
