pragma solidity ^0.5.9;

// ChunkedFiles Validator

contract Validator{
    
    struct file_info {
        uint size;
        bytes32 merkle_root;
    }
    
    uint public chunk_size;
    mapping(string => file_info) public files_infos;
	
	// constructs a validator
    constructor(uint _chunk_size) public {
        chunk_size = _chunk_size;
    }
    
	// add file to the validator
    function add_file_info(string calldata _file_name, uint _size, bytes32 _merkle_root) external {
        file_info memory _file_info = file_info(_size, _merkle_root);
        files_infos[_file_name] = _file_info;
    }

	// get the number of chunks in a file
    function get_chunks_num(string calldata _file_name) view external returns(uint) {
        return uint((int(files_infos[_file_name].size) - 1) / int(chunk_size) + 1);
    }
	
	// get the file name from the question
    function file_name(bytes memory question) pure internal returns(string memory){
        uint len = uint8(question[0]);
        bytes memory file_name_bytes = new bytes(len);
        for (uint i = 0; i < len; i++) {
            file_name_bytes[i] = question[i+1];
        }
        string memory _file_name = string(file_name_bytes);
        return _file_name;
    }

	// get the chunk number from the question
    function chunk_num(bytes memory question) pure internal returns(uint) {
        uint len = uint8(question[0]);
        bytes memory chunk_num_bytes = new bytes(question.length - (len + 1));
        for (uint i = 0; i < question.length - (len + 1); i++) {
            chunk_num_bytes[i] = question[len + 1 + i];
        }
        uint _chunk_num = 0;
        for (uint i = 0; i < chunk_num_bytes.length; i++) {
            _chunk_num = _chunk_num + uint8(chunk_num_bytes[i]) * ((2 ** 8) ** (chunk_num_bytes.length - (i + 1)));
        }
        return _chunk_num;
    }

	// get the high of the merkle tree of a file with a given size
    function high(uint size) view internal returns(uint) {
        uint number_of_chunks = uint((int(size) - 1) / int(chunk_size) + 1);
        uint _high = 1;
        if (number_of_chunks == 1) {
            _high = 2;
        }
        else {
            uint two_to_the = 1;
            while(two_to_the < number_of_chunks) {
                _high = _high + 1;
                two_to_the = two_to_the * 2;
            }
        }
        return _high;
    }

	// a casting function
    function bytes32array_to_bytes(bytes32[] memory bytes32array) pure internal returns(bytes memory) {
        uint nonzero_bytes = uint8(bytes32array[0][0]);
        bytes memory _bytes = new bytes((bytes32array.length - 2) * 32 + nonzero_bytes);
        uint ind = 0;
        for (uint i = 0; i < bytes32array.length - 2; i++) {
            for(uint j = 0; j < 32; j++) {
                _bytes[ind] = bytes32array[i+1][j];
                ind = ind + 1;
            }
        }
        for (uint j = 0; j < nonzero_bytes; j++) {
            _bytes[ind] = bytes32array[bytes32array.length-1][j];
            ind = ind + 1;
        }
        return _bytes;
    }
    
	// check if a question is valid
    function is_valid_question(bytes32[] calldata _question) view external returns(bool){
        bytes memory question = bytes32array_to_bytes(_question);
        string memory _file_name = file_name(question);
		// does the validator has the files' info?
        if (files_infos[_file_name].size == 0 && files_infos[_file_name].merkle_root == bytes32(0)) {
            return false;
        }
        uint _chunk_num = chunk_num(question);
		// does the file has that chunk?
        if (_chunk_num >= uint((int(files_infos[_file_name].size) - 1) / int(chunk_size) + 1)) { // round_up(files_infos[file_name].size / chunk_size)
            return false;
        }
        return true;
    }
    
	// get the chunk size from the answer
    function answer_chunk_size(bytes memory answer) pure internal returns(uint) {
        uint chunk_size_num_of_bytes = uint8(answer[0]);
        bytes memory chunk_size_bytes = new bytes(chunk_size_num_of_bytes);
        for (uint i = 0; i < chunk_size_num_of_bytes; i++) {
            chunk_size_bytes[i] = answer[i+1];
        }
        uint _answer_chunk_size = 0;
        for (uint i = 0; i < chunk_size_num_of_bytes; i++) {
            _answer_chunk_size = _answer_chunk_size + uint8(chunk_size_bytes[i]) * ((2 ** 8) ** (chunk_size_num_of_bytes - (i + 1)));
        }
        return _answer_chunk_size;
    }

	// check if the answer is valid (assuming the question is valid)
    function is_answer_correct(bytes32[] calldata _question, bytes32[] calldata _answer) view external returns(bool){
        bytes memory question = bytes32array_to_bytes(_question);
        bytes memory answer = bytes32array_to_bytes(_answer);
        string memory _file_name = file_name(question);
        uint _chunk_num = chunk_num(question);
        uint _high = high(files_infos[_file_name].size);
        
		// check the answer's length
		
        if (answer.length == 0) {
            return false;
        }
        
        if (answer.length < 1+uint8(answer[0])) {
            return false;
        }
        
        uint _answer_chunk_size = answer_chunk_size(answer);
        
        if (answer.length != 1+uint8(answer[0])+_answer_chunk_size + 32 * (_high + 1)) {
            return false;
        }
        
        bytes memory chunk_num_bits = new bytes(_high-1);
        uint tmp_chunk_num = _chunk_num;
        byte bit;
        for (uint i = 0; i < _high-1; i++) {
            bit = byte(uint8(tmp_chunk_num % 2));
            tmp_chunk_num = tmp_chunk_num / 2;
            chunk_num_bits[i] = bit;
        }
        
        bytes memory chunk = new bytes(_answer_chunk_size);
        for (uint i = 0; i < _answer_chunk_size; i++) {
            chunk[i] = answer[(1+uint8(answer[0]))+i];
        }
        
        _answer_chunk_size = 1+uint8(answer[0])+_answer_chunk_size;
        
        bytes memory hash = new bytes(32);
        for(uint i = 0; i < 32; i++) {
            hash[i] = answer[_answer_chunk_size + i];
        }
        bytes32 hash32;
        assembly {
            hash32 := mload(add(hash, 32))
        }
		// does the hash of the chunk correct?
        if (keccak256(chunk) != hash32) {
            return false;
        }
        bytes memory path_hash = hash;
        bytes memory tmp_hash = new bytes(32);
        for (uint i = 0; i < _high-1; i++) {
            tmp_hash = new bytes(32);
            for (uint j = 0; j < 32; j++) {
                tmp_hash[j] = answer[_answer_chunk_size + 32 * (i + 1) + j];
            }
            if (chunk_num_bits[i] == byte(0)) {
                path_hash = abi.encodePacked(keccak256(abi.encodePacked(path_hash, tmp_hash)));
            }
            else { // chunk_num_bits[i] == byte(1)
                path_hash = abi.encodePacked(keccak256(abi.encodePacked(tmp_hash, path_hash)));
            }
        }
        bytes32 path_hash_32;
        assembly {
            path_hash_32 := mload(add(path_hash, 32))
        }
		// does the merkle path leads to the merkle root?
        if (path_hash_32 != files_infos[_file_name].merkle_root) {
            return false;
        }
        return true;
        
    }
}