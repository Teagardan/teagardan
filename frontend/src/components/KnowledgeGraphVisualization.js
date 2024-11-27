import React, { useEffect, useState, useRef } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import {
  fetchKnowledgeGraph,
  updateKnowledgeGraph,
  selectKnowledgeGraph,
} from '../redux/knowledgeGraphSlice';  // Redux interaction
import { ForceGraph2D } from 'react-force-graph'; // Or your preferred graph visualization library
import {
  Box,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  TextField,
  DialogActions,
  Typography,
} from '@mui/material'; // Import UI elements (replace with your UI library if needed)

const KnowledgeGraphVisualization = () => {
  const dispatch = useDispatch();
  const graphData = useSelector(selectKnowledgeGraph);
  const fgRef = useRef();
  const [editDialogOpen, setEditDialogOpen] = useState(false);
  const [newNodeName, setNewNodeName] = useState('');
  const [searchQuery, setSearchQuery] = useState(''); // New state for search


  useEffect(() => {
    dispatch(fetchKnowledgeGraph()); // Fetch data on component mount
  }, [dispatch]);



  const handleNodeClick = (node) => {
    // Implement node click behavior (e.g., open a details panel, expand/collapse)
    console.log("Clicked node:", node);
  };



  const handleLinkClick = (link) => {
    console.log('Clicked link:', link)
  };


  const handleAddNode = () => {
    setEditDialogOpen(true); // Open the dialog for adding a new node
  };




  const handleDialogClose = () => {
    setEditDialogOpen(false);
    setNewNodeName(''); // Clear input when dialog is closed
  };



  const handleDialogSubmit = () => {
    // Dispatch an action to add the node to the knowledge graph
    if (newNodeName.trim() !== "") { //Prevent empty nodes.
        dispatch(updateKnowledgeGraph({ newNodeName }));
        setNewNodeName(''); // Reset input.  
    }
    setEditDialogOpen(false); //Close the dialog.
  };


  const handleSearchChange = (event) => {
    setSearchQuery(event.target.value); // Update local component's search state.
  };


  const handleNodeSearch = () => {
    // In a more complex implementation, perform search on the backend using searchQuery.
    if(searchQuery){

        const foundNode = graphData.nodes.find(node => node.id.toLowerCase().includes(searchQuery.toLowerCase()));
        if(foundNode){
            fgRef.current.centerAt(foundNode.x, foundNode.y, 1000); // Smooth centering animation.
            fgRef.current.zoom(8, 2000); //Optional zoom for better focus.
        } else{
            alert("No node found."); //Inform user
        }
    }
  };






  // Default graph configuration:
  const defaultGraphProps = {
    nodeAutoColorBy: "group",  //Or type, or whatever grouping makes sense.
    linkDirectionalArrowLength: 5,
    linkDirectionalArrowRelPos: 0.5,
    enableNodeDrag: true,
    onNodeClick: handleNodeClick,
    onLinkClick: handleLinkClick

  };

  // Updated graphData with filtered nodes:
  const filteredGraphData = {
    nodes: graphData.nodes,
    links: graphData.links
  }


  return (
    <div>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
        <Typography variant="h5" component="h2" sx={{ flexGrow: 1 }}>Knowledge Graph</Typography>

        <TextField
          label="Search Nodes"
          variant="outlined"
          size="small"
          value={searchQuery}
          onChange={handleSearchChange}
          sx={{ mr: 2, width: 200 }} // Add spacing and sizing
        />
        <Button variant="contained" onClick={handleNodeSearch} size="small">Search</Button>

        <Button onClick={handleAddNode} variant="outlined" color="primary" size="small">Add Node</Button>
        <Dialog open={editDialogOpen} onClose={handleDialogClose}>
        <DialogTitle>Add New Node</DialogTitle>
        <DialogContent>

            <TextField
                autoFocus
                margin="dense"
                id="name"
                label="Node Name"
                type="text"
                fullWidth
                variant="standard"
                value={newNodeName}
                onChange={(e) => setNewNodeName(e.target.value)}
            />
        </DialogContent>
        <DialogActions>
            <Button onClick={handleDialogClose}>Cancel</Button>
            <Button onClick={handleDialogSubmit}>Add</Button>
        </DialogActions>
        </Dialog>
      </Box>
      
      {graphData && ( //Only render if graphData is loaded.
        <ForceGraph2D 
            graphData={filteredGraphData}  //Update with current graph data
            {...defaultGraphProps}
            ref={fgRef} // Assign ref to ForceGraph instance
        />
      )}


    </div>

  );
};



export default KnowledgeGraphVisualization;