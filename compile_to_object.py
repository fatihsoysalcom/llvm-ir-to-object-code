import subprocess
import sys

def compile_llvm_ir_to_object(llvm_ir_code, output_filename):
    """Compiles LLVM IR code to an object file using llc."""
    try:
        # Save LLVM IR to a temporary file
        with open("temp.ll", "w") as f:
            f.write(llvm_ir_code)

        # Command to invoke llc (LLVM static compiler)
        # -filetype=obj: specifies output format as object file
        # -o: specifies the output filename
        command = ["llc", "-filetype=obj", "-o", output_filename, "temp.ll"]
        
        # Execute the command
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        
        print(f"Successfully compiled {output_filename}")
        if result.stdout:
            print("LLC stdout:", result.stdout)
        if result.stderr:
            print("LLC stderr:", result.stderr)

    except FileNotFoundError:
        print("Error: 'llc' command not found. Please ensure LLVM is installed and 'llc' is in your PATH.", file=sys.stderr)
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Error during compilation: {e}", file=sys.stderr)
        print("LLC stdout:", e.stdout, file=sys.stderr)
        print("LLC stderr:", e.stderr, file=sys.stderr)
        sys.exit(1)
    finally:
        # Clean up temporary file
        import os
        if os.path.exists("temp.ll"):
            os.remove("temp.ll")

if __name__ == "__main__":
    # Example LLVM IR code for a simple function that adds two integers
    # This is a simplified representation of what a compiler might generate.
    example_llvm_ir = "\n"
    example_llvm_ir += "; ModuleID = 'example.ll'\n"
    example_llvm_ir += "source_filename = \"example.ll\"\n"
    example_llvm_ir += "target triple = \"x86_64-unknown-linux-gnu\"\n\n"
    example_llvm_ir += "define i32 @add(i32 %a, i32 %b) {\n"
    example_llvm_ir += "  %sum = add i32 %a, %b\n"
    example_llvm_ir += "  ret i32 %sum\n"
    example_llvm_ir += "}\n"

    output_object_file = "add.o"
    print("--- Compiling LLVM IR to Object Code ---")
    compile_llvm_ir_to_object(example_llvm_ir, output_object_file)
    print("----------------------------------------")
    print(f"An object file named '{output_object_file}' has been generated.")
    print("This file contains machine code instructions, but is not yet executable.")
