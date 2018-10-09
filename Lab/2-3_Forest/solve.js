function Node(val) {
    this.value = val;
    this.left = null;
    this.right = null;
}

function BinarySearchTree() {
    this.root = null;
}

BinarySearchTree.prototype.push = function(val) {
    var root = this.root;

    if (!root) {
        this.root = new Node(val);
        return;
    }

    var currentNode = root;
    var newNode = new Node(val);

    while (currentNode) {
        if (val < currentNode.value) {
            if (!currentNode.left) {
                currentNode.left = newNode;
                break;
            } else {
                currentNode = currentNode.left;
            }
        } else {
            if (!currentNode.right) {
                currentNode.right = newNode;
                break;
            } else {
                currentNode = currentNode.right;
            }
        }
    }

}

var bst = new BinarySearchTree();

for (i of "yuoteavpxqgrlsdhwfjkzi_cmbn") {
    bst.push(i);
}

var search_str = "DLLDLDLLLLLDLLLLRLDLLDLDLLLRRDLLLLRDLLLLLDLLRLRRRDLLLDLLLDLLLLLDLLRDLLLRRLDLLLDLLLLLDLLLRLDLLDLLRLRRDLLLDLLRLRRRDLLRDLLLLLDLLLRLDLLDLLRLRRDLLLLLDLLRDLLLRRLDLLLDLLLLLDLLRDLLRLRRDLLLDLLLDLLRLRRRDLLLLLDLLLLRLDLLLRRLRRDDLLLRRDLLLRRLRDLLLRLDLRRDDLLLRLDLLLRRRDLLRLRRRDLRRLD";
var now = bst.root;
var out = "";
for (i of search_str) {
    if (i == "D") {
        out += now.value
        now = bst.root;
    } else if (i == "L") {
        now = now.left;
    } else if (i == "R") {
        now = now.right;
    }
}
console.log("flag{" + out + "}");